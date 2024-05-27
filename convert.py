import sys
import json
import yaml
import dicttoxml
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox

def json_to_xml(json_data):
    xml_data = dicttoxml.dicttoxml(json_data, custom_root='root', attr_type=False)
    return xml_data.decode()
def xml_to_json(xml_data):
    root = ET.fromstring(xml_data)
    def xml_to_dict(element):
        return {element.tag: list(map(xml_to_dict, element)) or element.text}
    json_data = xml_to_dict(root)
    return json_data
def json_to_yaml(json_data):
    yaml_data=yaml.dump(json.data)
    return yaml_data
def yaml_to_json(yaml_data):
    json_data = yaml.safe_load(yaml_data)
    return json_data
def read_file(file_path):
    with open(file_path, 'r') as file:
        if file_path.endswith('.json'):
            return json.load(file), 'json'
        elif file_path.endswith('.xml'):
            return file.read(), 'xml'
        elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
            return yaml.safe_load(file), 'yaml'
        else:
            raise ValueError('Unsupported file format')
def write_file(data, file_path, data_type):
    with open(file_path, 'w') as file:
        if data_type == 'json':
            json.dump(data, file, indent=4)
        elif data_type == 'xml':
            file.write(data)
        elif data_type == 'yaml':
            yaml.dump(data, file)
        else:
            raise ValueError('Unsupported file format')
def convert(input_path, output_path):
    data, input_format = read_file(input_path)
    if output_path.endswith('.json'):
        if input_format == 'xml':
            data = xml_to_json(data)
        converted_data = json.dumps(data, indent=4)
        output_format = 'json'
    elif output_path.endswith('.xml'):
        if input_format == 'json':
            converted_data = json_to_xml(data)
        elif input_format == 'yaml':
            data = yaml_to_json(data)
            converted_data = json_to_xml(data)
        output_format = 'xml'
    elif output_path.endswith('.yaml') or output_path.endswith('.yml'):
        if input_format == 'xml':
            data = xml_to_json(data)
        converted_data = json_to_yaml(data)
        output_format = 'yaml'
    else:
        raise ValueError('Unsupported output file format')
    write_file(converted_data, output_path, output_format)


class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Data Converter')
        self.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout()

        self.label = QLabel('Select files to convert', self)
        layout.addWidget(self.label)

        self.btnOpenInput = QPushButton('Select Input File', self)
        self.btnOpenInput.clicked.connect(self.open_input_file)
        layout.addWidget(self.btnOpenInput)

        self.btnOpenOutput = QPushButton('Select Output File', self)
        self.btnOpenOutput.clicked.connect(self.open_output_file)
        layout.addWidget(self.btnOpenOutput)

        self.btnConvert = QPushButton('Convert', self)
        self.btnConvert.clicked.connect(self.convert_files)
        layout.addWidget(self.btnConvert)

        self.setLayout(layout)

    def open_input_file(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, 'Open Input File', '',
                                              'All Files (*);;JSON Files (*.json);;XML Files (*.xml);;YAML Files (*.yaml;*.yml)',
                                              options=options)
        if file:
            self.input_file = file
            self.label.setText(f'Input File: {file}')

    def open_output_file(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getSaveFileName(self, 'Save Output File', '',
                                              'JSON Files (*.json);;XML Files (*.xml);;YAML Files (*.yaml;*.yml)',
                                              options=options)
        if file:
            self.output_file = file
            self.label.setText(f'Output File: {file}')

    def convert_files(self):
        try:
            convert(self.input_file, self.output_file)
            QMessageBox.information(self, 'Success', 'File converted successfully!')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConverterApp()
    ex.show()
    sys.exit(app.exec_())

