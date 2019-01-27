import pymel.core as pm
import materials as materials

vray_material_lst = ['VrayMtl', 'VrayFresnel',
                     'VrayFlakeMtl', 'VrayBlendMtl', 'file']


class Converter:
    def __init__(self):
        pass

    @staticmethod
    def set_attr(attr, value):
        if attr.isLocked():
            attr.unlock()
            attr.set(value)
            attr.lock()
        else:
            attr.set(value)

    @staticmethod
    def pre_run():
        for vp_shad in pm.ls(type='lambert'):
            if vp_shad.hasAttr('vraySpecificSurfaceShader'):
                vray_shader_input = vp_shad.attr(
                    'vraySpecificSurfaceShader').inputs(plugs=True)
                shader_engine_output = vp_shad.attr(
                    'outColor').outputs(plugs=True)
                if len(vray_shader_input) == 1 and len(shader_engine_output) == 1:
                    pm.disconnectAttr(vray_shader_input[0])
                    pm.connectAttr(
                        vray_shader_input[0], shader_engine_output[0], force=True)

    @staticmethod
    def transfer_attr(source_attr, target_attr):
        inputs = source_attr.inputs(plugs=True)
        outputs = source_attr.outputs(plugs=True)
        if len(inputs) > 0:
            if target_attr.isLocked():
                target_attr.unlock()
                pm.connectAttr(inputs[0], target_attr, force=True)
                pm.disconnectAttr(inputs[0], source_attr, force=True)
                target_attr.lock()
            else:
                pm.connectAttr(inputs[0], target_attr, force=True)
                pm.disconnectAttr(inputs[0], source_attr, force=True)
        elif len(outputs) > 0:
            for output in outputs:
                pm.connectAttr(inputs[0], output, force=True)
        else:
            Converter.set_attr(target_attr, source_attr.get())

    @staticmethod
    def swap_nodes(source_node, target_node, attr_dict):
        for src_attr, tgt_attr in dict(attr_dict).items():
            print(source_node.attr(src_attr), target_node.attr(tgt_attr))
            Converter.transfer_attr(source_node.attr(
                src_attr), target_node.attr(tgt_attr))

    @staticmethod
    def convert_selected_material():
        selected_material = pm.selected()
        if not selected_material:
            pm.confirmDialog(title='User inputs invalid', icon='critical',
                             message='Please select atleast one Vray node',
                             button=['Ok'], defaultButton='Ok')
        else:
            vray_history_nodes = pm.listHistory(selected_material[0], ac=True)
            Converter.convert(vray_history_nodes)
            print('Converted selected Vray nodes and to RedShift nodes successfully')

    @staticmethod
    def convert(vray_materials):
        for source_material in vray_materials:
            if source_material.nodeType() == 'VrayMtl':
                rs_material = pm.createNode('RedshiftMaterial')
                src_name = source_material.name()
                Converter.swap_nodes(
                    source_material, rs_material, materials.mat_attr_dict)
                rs_material.refl_weight.set(0)
                Converter.rename(rs_material, src_name)

            elif source_material.nodeType() == 'VrayFresnel':
                rs_fresnel = pm.createNode('RedshiftFresnel')
                src_name = source_material.name()
                Converter.swap_nodes(
                    source_material, rs_fresnel, materials.fresnel_attr_dict)
                rs_fresnel.correct_intensity.set(0)
                Converter.rename(rs_fresnel, src_name)

            elif source_material.nodeType() == 'VrayFlakeMtl':
                rs_carpaint = pm.createNode('RedshiftCarPaint')
                src_name = source_material.name()
                Converter.swap_nodes(
                    source_material, rs_carpaint, materials.flake_attr_dict)
                rs_carpaint.clearcoat_weight.set(0)
                rs_carpaint.clearcoat_color.set([0, 0, 0])
                rs_carpaint.base_color.set([0, 0, 0])
                rs_carpaint.diffuse_weight.set(0)
                Converter.rename(rs_carpaint, src_name)
            elif source_material.nodeType() == 'VrayBlendMtl':
                rs_material_blender = pm.createNode('RedshiftMaterialBlender')
                src_name = source_material.name()
                Converter.swap_nodes(source_material, rs_material_blender, materials.blend_attr_dict)
                for i in range(1,6):
                    rs_material_blender.setAttr('additiveMode{}'.format(i))
                Converter.rename(rs_material_blender, src_name)

            elif source_material.nodeType() == 'file':
                new_filename = source_material.fileTextureName.get().replace('.tx','.tif')
                source_material.fileTextureName.set(new_filename)

    @staticmethod
    def convert_all():
        all_vray_materials = pm.ls(type=vray_material_lst)
        Converter.convert(all_vray_materials)
        print('Converted all Vray nodes to RedShift nodes successfully')
    @staticmethod
    def rename(node, src_name):
        node.rename(src_name+'_redshift')

    @staticmethod
    def deleteSurfaceLuminance():
        for lum in pm.ls(type='surfaceLuminance'):
            pm.delete(lum.name())   # No RedShift Support
