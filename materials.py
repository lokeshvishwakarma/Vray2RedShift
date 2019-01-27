mat_attr_dict = {
    # -------------Material
    'dc': 'diffuse_color',
    'dca': 'diffuse_weight',
    'ra': 'diffuse_roughness',
    'ic': 'emission_color',
    'rlc': 'refl_color',
    'rlca': 'refl_weight',
    'rlg': 'refl_roughness',
    'an': 'refl_aniso',
    'anr': 'refl_aniso_rotation',
    'rrc': 'refr_color',
    'rrca': 'refr_weight',
    'rior': 'refr_ior',
    # 'bmt': '',
    'bm': 'bump_input',
    # 'bmu': 'bump_multiplier',
    'om': 'opacity_color',
    'oc': 'outColor',
}

fresnel_attr_dict = {
    # -------------Fresnel
    'ior': 'ior',
    'bc': 'facing_color',
    'wc': 'perp_color',
    'oc': 'outColor',
}
flake_attr_dict = {
    # -------------Flakes
    'fcol': 'flake_color',
    'fgls': 'flake_gloss',
    'fdns': 'flake_density',
    'fscl': 'flake_scale',
    'oc': 'outColor',
}
blend_attr_dict = {
    # -------------Blend
    'bm': 'baseColor',
    'am': 'additiveMode1',
    'cm0': 'layerColor1',
    'ba0': 'blendColor1',
    'cm1': 'layerColor2',
    'ba1': 'blendColor2',
    'cm2': 'layerColor3',
    'ba2': 'blendColor3',
    'cm3': 'layerColor4',
    'ba3': 'blendColor4',
    'cm4': 'layerColor5',
    'ba4': 'blendColor5',
    'cm5': 'layerColor6',
    'ba5': 'blendColor6',
    'oc': 'outColor',
}
