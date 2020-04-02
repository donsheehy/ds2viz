from dsviz.styles import StyleSheet
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
default_styles = StyleSheet.fromyaml(dir_path + '/default_styles.yaml')
