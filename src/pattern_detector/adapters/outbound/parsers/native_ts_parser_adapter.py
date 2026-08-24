"""Native Layout- and AST-Aware Parser for TypeScript & Modern JavaScript."""

from __future__ import annotations

import os
import re
from typing import Any

from pattern_detector.domain.code_model import (
    CodeModel,
    TSClass,
    TSFunction,
    TSInterface,
    TSModule,
    TSTypeAlias,
)
from pattern_detector.domain.value_objects import Location

# Regex Patterns for TypeScript / JavaScript Parsing
RE_IMPORT = re.compile(r"^\s*import\s+(?:(?:type\s+)?(?:\{[^}]*\}|\*\s+as\s+\w+|\w+)\s+from\s+)?['\"]([^'\"]+)['\"]", re.MULTILINE)
RE_INTERFACE = re.compile(r"^\s*(?:export\s+)?interface\s+([A-Za-z0-9_]+)(?:<([^>]+)>)?(?:\s+extends\s+([^{]+))?\s*\{([^}]*)\}", re.MULTILINE)
RE_TYPE_ALIAS = re.compile(r"^\s*(?:export\s+)?type\s+([A-Za-z0-9_]+)(?:<([^>]+)>)?\s*=\s*([^;]+);", re.MULTILINE)
RE_CLASS = re.compile(r"^\s*(?:@\w+(?:\([^)]*\))?\s*)*(?:export\s+)?(?:abstract\s+)?class\s+([A-Za-z0-9_]+)(?:<[^>]+>)?(?:\s+extends\s+([A-Za-z0-9_]+))?(?:\s+implements\s+([^{]+))?\s*\{", re.MULTILINE)
RE_FUNCTION = re.compile(r"^\s*(?:export\s+)?(?:async\s+)?function(?:\s*\*|\s+)\s*([A-Za-z0-9_]+)\s*\(([^)]*)\)(?:\s*:\s*([^{]+))?\s*\{", re.MULTILINE)
RE_ARROW_CONST = re.compile(r"^\s*(?:export\s+)?const\s+([A-Za-z0-9_]+)\s*=\s*(?:async\s*)?\(([^)]*)\)(?:\s*:\s*([^=>]+))?\s*=>", re.MULTILINE)
RE_DECORATOR = re.compile(r"@([A-Za-z0-9_]+)(?:\([^)]*\))?")


class NativeTypeScriptParserAdapter:
    """Parses .ts, .tsx, .js, .jsx, .mts, .cts files into CodeModel AST representation."""

    SUPPORTED_EXTENSIONS = {".ts", ".tsx", ".js", ".jsx", ".mts", ".cts", ".mjs", ".cjs"}

    def parse_project(self, project_path: str, excludes: list[str] | None = None) -> CodeModel:
        model = CodeModel()
        excludes = [e.strip("/\\") for e in (excludes or []) if e.strip("/\\")]

        if os.path.isfile(project_path):
            self._parse_file(project_path, model)
            return model

        for root, dirs, files in os.walk(project_path):
            rel_root = os.path.relpath(root, project_path).replace("\\", "/")
            if rel_root == ".":
                rel_root = ""

            # In-place directory pruning
            dirs[:] = [
                d for d in dirs
                if not d.startswith(".")
                and d not in ("node_modules", "dist", "build", ".next", ".turbo", "coverage", ".docusaurus")
                and not any(
                    (rel_root + "/" + d).strip("/").startswith(ex)
                    or d == ex
                    for ex in excludes
                )
            ]

            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in self.SUPPORTED_EXTENSIONS and not file.endswith(".d.ts"):
                    full_path = os.path.join(root, file)
                    self._parse_file(full_path, model)

        return model

    def _parse_file(self, file_path: str, model: CodeModel) -> None:
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                raw_source = f.read()
        except Exception:
            return

        lines = raw_source.splitlines()
        line_count = len(lines)
        file_name = os.path.basename(file_path)
        module_name = os.path.splitext(file_name)[0]

        module = TSModule(
            path=file_path,
            name=module_name,
            raw_source=raw_source,
            line_count=line_count,
            location=Location(file_path=file_path, line=1, col=1),
        )

        # 1. Parse Imports
        for match in RE_IMPORT.finditer(raw_source):
            module.imports.append(match.group(1))

        # 2. Parse Interfaces
        for match in RE_INTERFACE.finditer(raw_source):
            iface_name = match.group(1)
            generics_str = match.group(2) or ""
            extends_str = match.group(3) or ""
            body_str = match.group(4) or ""

            line_no = self._get_line_number(raw_source, match.start())
            generics = [g.strip() for g in generics_str.split(",") if g.strip()]
            extends_list = [e.strip() for e in extends_str.split(",") if e.strip()]

            methods = []
            props = []
            for b_line in body_str.splitlines():
                clean = b_line.strip()
                if "(" in clean and ")" in clean:
                    methods.append(clean.split("(")[0].strip())
                elif ":" in clean:
                    props.append(clean.split(":")[0].strip())

            module.interfaces[iface_name] = TSInterface(
                name=iface_name,
                generics=generics,
                properties=props,
                methods=methods,
                extends_list=extends_list,
                location=Location(file_path=file_path, line=line_no, col=1),
            )

        # 3. Parse Type Aliases
        for match in RE_TYPE_ALIAS.finditer(raw_source):
            type_name = match.group(1)
            generics_str = match.group(2) or ""
            def_str = match.group(3).strip()

            line_no = self._get_line_number(raw_source, match.start())
            generics = [g.strip() for g in generics_str.split(",") if g.strip()]

            is_union = " | " in def_str or def_str.startswith("|")
            is_discriminated = is_union and ("kind:" in def_str or "type:" in def_str or "tag:" in def_str)
            is_mapped = "[" in def_str and " in " in def_str and "]" in def_str
            is_conditional = " extends " in def_str and "?" in def_str and ":" in def_str
            is_branded = "__brand" in def_str or "unique symbol" in def_str or "Brand<" in def_str

            module.types[type_name] = TSTypeAlias(
                name=type_name,
                generics=generics,
                raw_definition=def_str,
                is_union=is_union,
                is_discriminated=is_discriminated,
                is_mapped=is_mapped,
                is_conditional=is_conditional,
                is_branded=is_branded,
                location=Location(file_path=file_path, line=line_no, col=1),
            )

        # 4. Parse Classes
        for match in RE_CLASS.finditer(raw_source):
            cls_name = match.group(1)
            extends_name = match.group(2)
            implements_str = match.group(3) or ""

            line_no = self._get_line_number(raw_source, match.start())
            implements_list = [i.strip() for i in implements_str.split(",") if i.strip()]

            # Extract preceding decorators
            start_pos = max(0, match.start() - 200)
            prefix = raw_source[start_pos:match.start()]
            decorators = RE_DECORATOR.findall(prefix)

            module.classes[cls_name] = TSClass(
                name=cls_name,
                implements_list=implements_list,
                extends_name=extends_name,
                decorators=decorators,
                location=Location(file_path=file_path, line=line_no, col=1),
            )

        # 5. Parse Functions
        for match in RE_FUNCTION.finditer(raw_source):
            fn_name = match.group(1)
            params_str = match.group(2) or ""
            ret_type = (match.group(3) or "").strip()
            line_no = self._get_line_number(raw_source, match.start())

            is_async = "async" in raw_source[max(0, match.start() - 30):match.start()]
            is_type_guard = " is " in ret_type or "asserts " in ret_type
            params = [p.strip() for p in params_str.split(",") if p.strip()]

            # Calculate cyclomatic complexity
            body_start = match.end()
            body_snippet = raw_source[body_start:min(len(raw_source), body_start + 1000)]
            cc = self._calculate_complexity(body_snippet)

            module.functions[fn_name] = TSFunction(
                name=fn_name,
                params=params,
                return_type=ret_type,
                is_async=is_async,
                is_type_guard=is_type_guard,
                cyclomatic_complexity=cc,
                location=Location(file_path=file_path, line=line_no, col=1),
            )

        # 6. Parse Arrow Functions / Const Callables
        for match in RE_ARROW_CONST.finditer(raw_source):
            fn_name = match.group(1)
            params_str = match.group(2) or ""
            ret_type = (match.group(3) or "").strip()
            line_no = self._get_line_number(raw_source, match.start())

            is_async = "async" in raw_source[max(0, match.start() - 30):match.end()]
            is_type_guard = " is " in ret_type or "asserts " in ret_type
            params = [p.strip() for p in params_str.split(",") if p.strip()]

            if fn_name not in module.functions:
                module.functions[fn_name] = TSFunction(
                    name=fn_name,
                    params=params,
                    return_type=ret_type,
                    is_async=is_async,
                    is_type_guard=is_type_guard,
                    cyclomatic_complexity=1,
                    location=Location(file_path=file_path, line=line_no, col=1),
                )

        model.add_module(module)

    def _get_line_number(self, text: str, index: int) -> int:
        return text.count("\n", 0, index) + 1

    def _calculate_complexity(self, code_block: str) -> int:
        complexity = 1
        branch_patterns = [
            r"\bif\b", r"\belse\s+if\b", r"\bswitch\b", r"\bcase\b",
            r"\bfor\b", r"\bwhile\b", r"\bcatch\b", r"&&", r"\|\|", r"\?\?"
        ]
        for pat in branch_patterns:
            complexity += len(re.findall(pat, code_block))
        return complexity
