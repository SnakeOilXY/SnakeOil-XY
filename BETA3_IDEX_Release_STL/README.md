# BETA2 Release(outdated document)

## What changed from Beta1

- Better 2020 gantry.
- New option for 1515 gantry with huge performance boost(see shaper test result below).
- New option for 1515 bed frame.
- New Z rail block mounting with limiter by default. This will keep the bed from tilting too much that cause the z probe cannot reach the bed.
- Better sherpa mini extruder mounter with 16mm shorter filament path.
- Added quick release front door and panel mounts.

![Banner](./../Doc/img/gantry-compare.png)

## What you need to reprint if you already have beta1 parts

- Z block mount
  - <code>1x_z-rail-block-mount-right-with-limiter.stl</code>
  - <code>2x_z-rail-block-mount-left-with-limiter.stl</code>
- Y carrier
  - <code>1x_y-carrier-bottom-left.stl</code>
  - <code>1x_y-carrier-bottom-right.stl</code>
  - <code>1x_y-carrier-top-left.stl</code>
  - <code>1x_y-carrier-top-right.stl</code>
- Extruder carrier parts
  - <code>1x_extruder-cable-support.stl</code>
  - <code>2x_extruder-belt-clamp.stl</code>
  - <code>2x_extruder-belt-tesioner.stl</code>
  - <code>1x_extruder-back-plate.stl</code>
  - <code>1x_extruder-front-plate.stl</code>
  - <code>And Sherpa mini mounter parts</code>

## What will be keep/change/added on later stable release

- Parts are tested and will not change on stable release
  - Motion system (XYZ) axis parts
  - Toolhead parts
  - Back and bottom panels/electronics mounter
- Parts are not tested, might change on later release
  - None
- Parts will be added later
  - Parts for 250mm3 machine size
  - Neopixel mount
  - Mounter to feed filament from outside enclosure
  - AIO filament sensor(jam/runout/fil.width detect)
  - Nozzle brush
- Parts will be replaced
  - None

## Parts printing

- Material : PETG, ABS, PC or anything you think will withstand the chamber temp you need.

- Recommended slicer setting:
  - Layer height : 0.2mm
  - Wall lines count : 5
  - Top/Bottom layers : 5
  - Infill : Gyroid 30%
  - Support placement : Touching d plate only

## Assembly, build help and bug report

- I don't have enough time to make the document atm. I will try to add document and build manual after finished design all the incomplete machine parts.
- For build log, help, and bug report please using [Our discord server](https://discord.gg/WZVP2HuAag)
