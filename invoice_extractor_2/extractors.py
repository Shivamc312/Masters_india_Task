import re
from dateutil.parser import parse as date_parse
import json

class GenericFieldExtractor:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = json.load(f)

    def extract_field(self, text: str, field_name: str):
        field = self.config.get(field_name)
        if not field:
            return None

        lines = text.splitlines()

        for i, line in enumerate(lines):
            for pattern in field.get("patterns", []):
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    group_index = field.get("group", 0)
                    raw_value = match.group(group_index)
                    if raw_value.strip() == "" and i + 1 < len(lines):
                        raw_value = lines[i + 1].strip()  # Take next line
                    if field.get("parse_date"):
                        try:
                            return date_parse(raw_value, fuzzy=True).strftime("%Y-%m-%d")
                        except:
                            continue
                    return raw_value
        return None

    def extract_line_items(self, text: str, config: dict):
        lines = text.splitlines()
        start_re = re.compile(config.get("start_pattern", ""), re.IGNORECASE)
        end_re = re.compile(config.get("end_pattern", ""), re.IGNORECASE)
        line_re = re.compile(config.get("line_pattern", ""))

        start_index, end_index = None, None

        # Find the start and end of the item table
        for i, line in enumerate(lines):
            if start_index is None and start_re.search(line):
                start_index = i
            elif start_index is not None and end_re.search(line):
                end_index = i
                break

        if start_index is None or end_index is None:
            return []

        line_items = []
        for line in lines[start_index + 1:end_index]:
            match = line_re.search(line)
            if match:
                item = {}
                for i, field in enumerate(config.get("fields", [])):
                    item[field] = match.group(i + 1)
                line_items.append(item)
        return line_items

    def extract_all_fields(self, text: str):
        result = {}
        for field_name, field_config in self.config.items():
            if field_name == "line_items":
                result[field_name] = self.extract_line_items(text, field_config)
            else:
                result[field_name] = self.extract_field(text, field_name)
        return result
