# Quick references to BOM part types.  Also provides type hinting in the BomPart dataclass
PRINTED_MAIN = "main"
PRINTED_ACCENT = "accent"
PRINTED_UNKNOWN_COLOR = "unknown"

COLOR_OVERRIDES = {
    "BETA3_Standard_Release_STL/STLs/E-axis/hotend-mount-for-sherpa-mini/cooper-head/1x_cooper-head-mount-mod.stl": PRINTED_MAIN,
    "BETA3_Standard_Release_STL/STLs/E-axis/hotend-mount-for-sherpa-mini/cooper-head/1x_copper-head-support-a.stl": PRINTED_UNKNOWN_COLOR,
    "BETA3_Standard_Release_STL/STLs/E-axis/hotend-mount-for-sherpa-mini/cooper-head/1x_copper-head-support-b.stl": PRINTED_UNKNOWN_COLOR,
    "BETA3_Standard_Release_STL/STLs/E-axis/sherpa-mini-extruder/back-body.stl": PRINTED_UNKNOWN_COLOR,
    "BETA3_Standard_Release_STL/STLs/E-axis/sherpa-mini-extruder/filament-arm.stl": PRINTED_UNKNOWN_COLOR,
    "BETA3_Standard_Release_STL/STLs/E-axis/sherpa-mini-extruder/front-body.stl": PRINTED_UNKNOWN_COLOR,
    "BETA3_Standard_Release_STL/STLs/E-axis/sherpa-mini-extruder/main-body-e3d-collet.stl": PRINTED_UNKNOWN_COLOR,
    "BETA3_Standard_Release_STL/STLs/E-axis/sherpa-mini-extruder/main-body-triangle-lab-collet.stl": PRINTED_UNKNOWN_COLOR,
    "BETA3_Standard_Release_STL/STLs/Panels/Back-panel/Bottom/250_MACHINE_ONLY_2x_gasket-side.stl": PRINTED_ACCENT,
    "BETA3_Standard_Release_STL/STLs/Panels/Bottom-panel/1x_side-panel-connector.stl": PRINTED_ACCENT,
    "BETA3_Standard_Release_STL/STLs/Panels/Bottom-panel/4x_foot_insert_TPU.stl": PRINTED_UNKNOWN_COLOR,
    "BETA3_Standard_Release_STL/STLs/XY-axis/generic-x-endstop/1x_x-endstop-base.stl": PRINTED_ACCENT,
    "BETA3_Standard_Release_STL/STLs/XY-axis/y-carrier-CF/2x_mounting-block.stl": PRINTED_UNKNOWN_COLOR,
    "BETA3_Standard_Release_STL/STLs/Z-axis/6x_bed-spring-top-spacer.stl": PRINTED_UNKNOWN_COLOR,  # Remove?
    "BETA3_Standard_Release_STL/STLs/Z-axis/6x_bedspring-bottom-spacer.stl": PRINTED_UNKNOWN_COLOR,  # Remove?
    "BETA3_Standard_Release_STL/STLs/Z-axis/bed-frame-2020/2x_bed-extrusion-end-left.stl": PRINTED_MAIN,
    "BETA3_Standard_Release_STL/STLs/Z-axis/bed-frame-2020/2x_bed-extrusion-end-right.stl": PRINTED_MAIN,
    "BETA3_Standard_Release_STL/STLs/Z-axis/bed-frame-2020/bed-arm-threaded-ball-coupler(default-in-beta-2)/3x_bed-frame-top-arm.stl": PRINTED_MAIN,
    "BETA3_Standard_Release_STL/STLs/Z-axis/recommended-bed-frame-1515/bed-arm-threaded-ball-coupler(default-in-beta-2)/3x_threaded-ball-spacer.stl": PRINTED_ACCENT,
    "BETA3_Standard_Release_STL/STLs/Z-axis/z-counter-weight/1x_top-bearing-arm.stl": PRINTED_MAIN,
    "BETA3_Standard_Release_STL/STLs/Z-axis/z-counter-weight/1x_z-rail-block-mount-right-with-limiter-dual(default-in-beta-2).stl": PRINTED_MAIN,
    "BETA3_Standard_Release_STL/STLs/Panels/Front-panel/2x_knob.stl": PRINTED_MAIN,
    "BETA3_Standard_Release_STL/STLs/Z-axis/bed-frame-2020/1x_bed-wago-mounter.stl": PRINTED_ACCENT,
    "BETA3_Standard_Release_STL/STLs/Z-axis/bed-frame-makerbeamxl/1x_wago-mounter.stl": PRINTED_ACCENT,
    "BETA3_Standard_Release_STL/STLs/Z-axis/recommended-bed-frame-1515/1x_wago-mounter.stl": PRINTED_ACCENT,
}