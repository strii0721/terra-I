import adsk.core, adsk.fusion, traceback
import os
import xml.etree.ElementTree as ET
import re
import xml.dom.minidom as minidom

ui = None

def run(context):
    global ui
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        root = design.rootComponent
        exportMgr = design.exportManager

        # 设置导出文件夹
        folder = os.path.expanduser("~/Desktop")
        os.makedirs(folder, exist_ok=True)

        # 创建 XML 根节点
        xml_root = ET.Element("FusionAssembly")
        
        def sanitize_filename(name):
            return re.sub(r'[\\/*?:"<>| ]', '_', name)

        # 遍历所有 occurrence 并导出
        def export_occurrence(occurrence, parent_xml):
            name = occurrence.name.replace(" ", "_")
            component = occurrence.component
            transform = occurrence.transform.asArray()

            # 导出 STEP 文件（使用 Component）
            
            safe_name = sanitize_filename(name)
            step_filename = f"{safe_name}.step"
            step_path = os.path.join(folder, step_filename)
            step_options = exportMgr.createSTEPExportOptions(step_path, component)
            exportMgr.execute(step_options)

            # 写入 XML 节点
            node = ET.SubElement(parent_xml, "Part")
            node.set("name", name)
            node.set("component", component.name)
            node.set("stepFile", step_filename)

            transform_node = ET.SubElement(node, "Transform")
            transform_node.text = ",".join([str(val) for val in transform])

            # 递归处理子组件
            for child_occ in occurrence.childOccurrences:
                export_occurrence(child_occ, node)

        # 处理顶层所有 occurrence
        for occ in root.occurrences:
            export_occurrence(occ, xml_root)

        # 保存结构 XML 文件
        xml_path = os.path.join(folder, "assembly_structure.xml")
        rough_string = ET.tostring(xml_root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        with open(xml_path, 'w', encoding='utf-8') as f:
            f.write(reparsed.toprettyxml(indent="  "))

            ui.messageBox(f"导出完成！\n目录: {folder}")

    except:
        if ui:
            ui.messageBox('脚本出错:\n{}'.format(traceback.format_exc()))
