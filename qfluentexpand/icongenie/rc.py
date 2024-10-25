#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


from PyQt5.QtCore import QCoreApplication
from PySide6.QtCore import Qt, QFileInfo, QDir, QResource
import os
import sys
import importlib
import xml.etree.ElementTree as ET
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional, Dict



class QRC:

    def __init__(self, file):
        self.file = file
        self.app = QCoreApplication(sys.argv)

    def addFile(self, file, prefix):
        self.app.addResource(QResource.AddFile, prefix, file)

    def read(self):
        return self.resource.entryList()

    def write(self, content, prefix="/icons"):
        self.resource.setFileName(self.file)
        self.resource.registerResource(content)

    def readQRC(self):
        result = []
        if os.path.exists(self.file):
            with open(self.file, 'r') as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    elif "<file>" not in line:
                        return line
                    line = line.lstrip("<file>")
                    line = line.rstrip("</file>")
                    result.append(line)

        return result
    @classmethod
    def writeQRC(self, file, content, prefix="/icons"):
        with open(file, 'w') as f:
            f.write('<RCC>\n')
            f.write(f'    <qresource prefix="{prefix}">\n')
            for i in content:
                f.write(f'        <file>{i}</file>\n')
            f.write('    </qresource>\n')
            f.write('</RCC>\n')




class Resource:

    def __init__(self, file):
        self.file = file
        self.state = 0     # 0: not loaded, 1: loaded successfully, 2: failed to load, 3: empty file

    def load(self):
        file = self.file
        if not os.path.exists(file):
            raise Exception(f"File does not exist: {file}")
        try:
            spec = importlib.util.spec_from_file_location("resource", file)
            resource = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(resource)
            sys.modules["resource"] = resource

            print("Resource file imported successfully")
            self.state = 1
        except NameError as e:
            if "name 'qt_resource_struct' is not defined" in str(e):
                print(e)
                self.state = 3
        except ImportError as e:
            self.state = 2
            raise Exception(f"Failed to import resource file: {e}")

    def getImages(self, prefix=":/icons"):
        def getList(root_dir):
            tmp = []
            if root_dir.exists():
                entries = root_dir.entryList()
                # print("\n根目录内容:")
                if entries:
                    for entry in entries:
                        # print(f"- {entry}")
                        tmp.append(entry)
            return tmp

        if self.state == 0:
            self.load()
        elif self.state == 2:
            return None
        elif self.state == 3:
            return {}

        root_dir = QDir(prefix)
        # print("\n根目录内容:", prefix)
        return list(set(getList(root_dir)))

    def show(self, prefix=":/icons"):
        file = self.file
        if not os.path.exists(file):
            raise Exception(f"File does not exist: {file}")
        try:
            spec = importlib.util.spec_from_file_location("resource", file)
            resource = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(resource)
            sys.modules["resource"] = resource

            print("资源文件导入成功")
        except ImportError as e:
            raise Exception(f"Failed to import resource file: {e}")

        # 2. 检查根目录内容
        root_dir = QDir(prefix)
        if root_dir.exists():
            print("\n根目录内容:")
            entries = root_dir.entryList()
            if entries:
                for entry in entries:
                    print(f"- {entry}")
            else:
                print("目录为空")
        else:
            print("根目录不存在")


@dataclass
class QrcResource:
    """Represents a single resource entry in a QRC file"""
    file_path: str
    alias: Optional[str]
    prefix: str
    lang: Optional[str]
    full_path: str
    exists: bool = True

    @property
    def is_image(self) -> bool:
        """Check if the resource is an image file"""
        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg'}
        return Path(self.file_path).suffix.lower() in image_extensions

    @property
    def is_icon(self) -> bool:
        """Check if the resource is likely to be an icon"""
        # Check file name patterns commonly used for icons
        name = Path(self.file_path).stem.lower()
        icon_patterns = {'icon', 'ico', 'logo', 'symbol', 'favicon'}

        # Check if any icon pattern is in the file name
        has_icon_name = any(pattern in name for pattern in icon_patterns)

        # Check if file is in an icon directory
        in_icon_dir = any(part in ['icons', 'icon'] for part in Path(self.file_path).parts)

class QrcParser:
    """Parser for Qt Resource Collection (.qrc) files"""

    def __init__(self, qrc_path: str):
        """Initialize parser with path to .qrc file"""
        self.qrc_path = Path(qrc_path)
        self.base_dir = self.qrc_path.parent
        self.resources: List[QrcResource] = []
        self._parse()

    def _parse(self):
        """Parse the QRC file and extract all resources"""
        try:
            tree = ET.parse(self.qrc_path)
            root = tree.getroot()

            # Process each qresource element
            for qresource in root.findall('qresource'):
                prefix = qresource.get('prefix', '/')
                lang = qresource.get('lang', None)

                # Process each file element within qresource
                for file_elem in qresource.findall('file'):
                    file_path = file_elem.text
                    if file_path is None:
                        continue

                    # Get optional alias
                    alias = file_elem.get('alias', None)

                    # Check if file exists
                    full_path = self.base_dir / file_path
                    exists = full_path.exists()

                    resource = QrcResource(
                        file_path=file_path,
                        alias=alias,
                        prefix=prefix,
                        lang=lang,
                        full_path=str(full_path),
                        exists=exists
                    )
                    self.resources.append(resource)

        except ET.ParseError as e:
            raise ValueError(f"Failed to parse QRC file: {e}")
        except Exception as e:
            raise ValueError(f"Error processing QRC file: {e}")

    def has_icon(self, icon_path: str, check_content: bool = False) -> bool:
        """
        Check if the specified icon file exists in the QRC file

        Args:
            icon_path: Path to the icon file to check
            check_content: If True, also verify the file is actually an image

        Returns:
            bool: True if the icon exists, False otherwise
        """
        # Normalize path for comparison
        icon_path = str(Path(icon_path))

        # Check if exact path exists
        for resource in self.resources:
            if resource.file_path == icon_path and resource.exists:
                if check_content:
                    return resource.is_image
                return True

        return False

    def find_icons(self, include_missing: bool = False) -> List[QrcResource]:
        """
        Find all resources that appear to be icons

        Args:
            include_missing: If True, include icons that don't exist on disk

        Returns:
            List[QrcResource]: List of icon resources
        """
        icons = []
        for resource in self.resources:
            if resource.is_icon and (include_missing or resource.exists):
                icons.append(resource)
        return icons

    def get_icon_summary(self) -> str:
        """Generate a summary of icon resources"""
        icons = self.find_icons(include_missing=True)

        summary = ["Icon Resources:"]
        if not icons:
            summary.append("  No icons found")
            return "\n".join(summary)

        # Group by prefix
        prefix_groups: Dict[str, List[QrcResource]] = {}
        for icon in icons:
            if icon.prefix not in prefix_groups:
                prefix_groups[icon.prefix] = []
            prefix_groups[icon.prefix].append(icon)

        # Generate summary by prefix
        for prefix, resources in prefix_groups.items():
            summary.append(f"\nPrefix: {prefix}")
            for resource in resources:
                status = "✓" if resource.exists else "✗"
                alias_info = f" (alias: {resource.alias})" if resource.alias else ""
                summary.append(f"  {status} {resource.file_path}{alias_info}")

        return "\n".join(summary)

    def validate(self) -> List[str]:
        """Validate the QRC file and return list of errors"""
        errors = []

        # Check if all referenced files exist
        for resource in self.resources:
            if not resource.exists:
                errors.append(f"Missing file: {resource.file_path}")

        return errors

    def get_resource_paths(self) -> List[str]:
        """Get list of all resource paths"""
        return [r.file_path for r in self.resources]

    def get_qt_resource_paths(self) -> List[str]:
        """Get list of Qt resource paths (with prefix)"""
        return [f":{r.prefix}/{r.alias or r.file_path}" for r in self.resources]

    def add_resource(self, file_path: str, prefix: str = '/', alias: Optional[str] = None):
        """Add a new resource to the QRC file"""
        if not self.qrc_path.exists():
            root = ET.Element('RCC')
            tree = ET.ElementTree(root)
        else:
            tree = ET.parse(self.qrc_path)
            root = tree.getroot()

        qresource = None
        for elem in root.findall('qresource'):
            if elem.get('prefix', '/') == prefix:
                qresource = elem
                break

        if qresource is None:
            qresource = ET.SubElement(root, 'qresource', {'prefix': prefix})

        file_elem = ET.SubElement(qresource, 'file')
        file_elem.text = str(Path(file_path))  # Normalize path
        if alias:
            file_elem.set('alias', alias)
        # file_elem.tail = '\n'

        self._write_tree(tree)
        self._parse()

    def remove_resource(self, file_path: str) -> bool:
        """Remove a resource from the QRC file"""
        tree = ET.parse(self.qrc_path)
        root = tree.getroot()

        removed = False
        for qresource in root.findall('qresource'):
            for file_elem in qresource.findall('file'):
                if file_elem.text == file_path:
                    qresource.remove(file_elem)
                    removed = True

        if removed:
            tree.write(self.qrc_path, encoding='utf-8', xml_declaration=True)
            self._parse()

        return removed

    def generate_summary(self) -> str:
        """Generate a summary of the QRC file contents"""
        summary = [f"QRC File: {self.qrc_path.name}"]
        summary.append(f"Total Resources: {len(self.resources)}")

        # Group by prefix
        prefix_groups = {}
        for resource in self.resources:
            if resource.prefix not in prefix_groups:
                prefix_groups[resource.prefix] = []
            prefix_groups[resource.prefix].append(resource)

        for prefix, resources in prefix_groups.items():
            summary.append(f"\nPrefix: {prefix}")
            for resource in resources:
                status = "✓" if resource.exists else "✗"
                alias_info = f" (alias: {resource.alias})" if resource.alias else ""
                lang_info = f" [lang: {resource.lang}]" if resource.lang else ""
                summary.append(f"  {status} {resource.file_path}{alias_info}{lang_info}")

        return "\n".join(summary)

    def _write_tree(self, tree: ET.ElementTree):
        root = tree.getroot()
        xml_str = ET.tostring(root, encoding='unicode').replace('</file>', '</file>\n')
        with open(self.qrc_path, 'w', encoding='utf-8') as f:
            f.write(xml_str)

    @staticmethod
    def create_new_qrc(file_path: str) -> 'QrcParser':
        """Create a new empty QRC file"""
        file_path = Path(file_path)

        # Create parent directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Create initial QRC structure
        root = ET.Element('RCC')
        tree = ET.ElementTree(root)

        # Write the file without XML declaration
        xml_str = ET.tostring(root, encoding='unicode')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(xml_str)

