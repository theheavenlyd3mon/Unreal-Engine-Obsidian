---
title: "UE 5.8 Python Scripting for Asset Pipeline Automation"
tags: [ue5, python, scripting, asset-pipeline, glb, skeletal-mesh, blueprint, import, automation]
source: "NeonGrid project — verified against UE 5.8.2"
status: "verified"
---

# UE 5.8 Python Scripting for Asset Pipeline Automation

> Practical, verified patterns for automating GLB import, Blueprint creation, and level setup via Python in UE 5.8.
> Derived from the NeonGrid project's `unreal/import_neongrid.py` and `unreal/setup_neongrid_level.py`.

## Overview

UE 5.8's Python scripting API (`unreal.AssetToolsHelpers`, `unreal.EditorAssetLibrary`, `unreal.EditorLevelLibrary`) enables full automation of the asset import → Blueprint creation → level placement pipeline. This is particularly valuable for projects with many similar assets (e.g., mechs, weapons, tiles).

## Key Verified Patterns

### 1. GLB Import (Static + Skeletal Meshes)

```python
import unreal

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
editor_asset_lib = unreal.EditorAssetLibrary()

# Static mesh import (weapons, tiles, environments)
def import_static_mesh(glb_path, asset_name, destination_path):
    """Import a GLB file as a static mesh."""
    ui = unreal.FbxImportUI()
    ui.import_mesh = True
    ui.import_as_skeletal = False
    ui.mesh_type_to_import = unreal.FBXImportType.FBXIT_STATIC_MESH
    ui.import_materials = False  # Materials handled separately
    ui.import_textures = False
    ui.import_animations = False

    # Critical import settings (verified in NeonGrid)
    ui.static_mesh_import_data.set_editor_property("convert_scene", True)
    ui.static_mesh_import_data.set_editor_property("import_uniform_scale", 1.0)

    task = unreal.AssetImportTask()
    task.filename = glb_path
    task.destination_path = destination_path
    task.automated = True
    task.save = True
    task.replace_existing = True
    task.options = ui

    asset_tools.import_asset_tasks([task])

    asset_path = f"{destination_path}/{asset_name}"
    asset_data = editor_asset_lib.find_asset_data(asset_path)
    if asset_data:
        sm = editor_asset_lib.load_asset(asset_path)
        if sm:
            bounds = sm.get_bounds()
            log(f"  [OK] {asset_name}: bounds={bounds.box_extent.x:.1f}x{bounds.box_extent.y:.1f}x{bounds.box_extent.z:.1f}")
            return True
    log(f"  [FAIL] {asset_name}: import failed")
    return False

# Skeletal mesh import (mechs, kaiju — requires rigging)
def import_skeletal_mesh(glb_path, asset_name, destination_path):
    """Import a GLB file as a skeletal mesh."""
    ui = unreal.FbxImportUI()
    ui.import_mesh = True
    ui.import_as_skeletal = True
    ui.mesh_type_to_import = unreal.FBXImportType.FBXIT_SKELETAL_MESH
    ui.import_materials = False
    ui.import_textures = False
    ui.import_animations = False

    # Critical import settings (verified in NeonGrid)
    ui.skeletal_mesh_import_data.set_editor_property("convert_scene", True)
    ui.skeletal_mesh_import_data.set_editor_property("import_uniform_scale", 1.0)

    task = unreal.AssetImportTask()
    task.filename = glb_path
    task.destination_path = destination_path
    task.automated = True
    task.save = True
    task.replace_existing = True
    task.options = ui

    asset_tools.import_asset_tasks([task])

    asset_path = f"{destination_path}/{asset_name}"
    asset_data = editor_asset_lib.find_asset_data(asset_path)
    if asset_data:
        sm = editor_asset_lib.load_asset(asset_path)
        if sm:
            bounds = sm.get_bounds()
            try:
                num_bones = len(sm.skeleton.get_bone_names()) if sm.skeleton else 0
            except:
                num_bones = 0
            log(f"  [OK] {asset_name}: bounds={bounds.box_extent.x:.1f}x{bounds.box_extent.y:.1f}x{bounds.box_extent.z:.1f}, bones={num_bones}")
            return True
    log(f"  [FAIL] {asset_name}: import failed")
    return False
```

### 2. Blueprint Class Creation from Imported Meshes

```python
def create_unit_blueprint(unit_name, is_skeletal=True):
    """Create a Blueprint class for a unit."""
    blueprint_factory = unreal.BlueprintFactory()
    if is_skeletal:
        blueprint_factory.set_editor_property("parent_class", unreal.Character)
    else:
        blueprint_factory.set_editor_property("parent_class", unreal.Actor)

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    bp_path = "/Game/NeonGrid/Blueprints/Units"

    # Ensure directory exists
    if not unreal.EditorAssetLibrary.does_directory_exist(bp_path):
        unreal.EditorAssetLibrary.make_directory(bp_path)

    blueprint = asset_tools.create_asset(
        asset_name=f"BP_{unit_name}",
        package_path=bp_path,
        asset_class=unreal.Blueprint,
        factory=blueprint_factory
    )

    if blueprint:
        unreal.EditorAssetLibrary.save_asset(f"{bp_path}/BP_{unit_name}")
        return True
    return False
```

### 3. Isometric Camera Setup

```python
ISO_ANGLE = 35.264  # degrees — standard isometric angle (arctan(1/√2))
ISO_YAW = 45  # degrees

def setup_isometric_camera(grid_width=15, grid_height=11, grid_size=100):
    """Set up the isometric camera in the level.

    NeonGrid uses 35.264° (arctan(1/√2)) pitch and 45° yaw —
    the standard isometric projection angle.
    """
    editor_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    world = editor_subsystem.get_editor_world()
    if not world:
        return None

    # Calculate camera position for isometric view
    camera_x = 0
    camera_y = -grid_width * grid_size
    camera_z = grid_height * grid_size * 1.5

    camera_pos = unreal.Vector(camera_x, camera_y, camera_z)
    camera_rot = unreal.Rotator(-ISO_ANGLE, ISO_YAW, 0)

    # Spawn camera actor
    camera_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.CameraActor,
        camera_pos,
        camera_rot
    )
    if camera_actor:
        camera_actor.set_actor_label("IsometricCamera")
        return camera_actor
    return None
```

### 4. Grid-Based Level Setup (Isometric Projection)

```python
GRID_WIDTH = 15
GRID_HEIGHT = 11
GRID_SIZE = 100  # Unreal units per grid cell

def get_grid_to_world(x, y):
    """Convert grid coordinates to world coordinates (isometric).

    Uses proper isometric projection:
    - World X = (x - y) * cos(30) * GRID_SIZE
    - World Y = (x + y) * sin(30) * GRID_SIZE
    """
    world_x = (x - y) * GRID_SIZE * 0.866  # cos(30)
    world_y = (x + y) * GRID_SIZE * 0.5    # sin(30)
    world_z = 0
    return unreal.Vector(world_x, world_y, world_z)

def place_tile(x, y, tile_name, world_pos):
    """Place a tile at the given grid position."""
    tile_path = f"/Game/NeonGrid/Tiles/{tile_name}"
    tile_asset = unreal.EditorAssetLibrary.load_asset(tile_path)
    if not tile_asset:
        return None

    editor_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    world = editor_subsystem.get_editor_world()
    if not world:
        return None

    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor,
        world_pos,
        unreal.Rotator(0, 0, 0)
    )
    if actor:
        actor.static_mesh_component.set_static_mesh(tile_asset)
        actor.set_actor_label(f"Tile_{x}_{y}_{tile_name}")
        return actor
    return None

def place_unit(x, y, unit_name, faction, world_pos):
    """Place a unit at the given grid position."""
    if faction == "player":
        unit_path = f"/Game/NeonGrid/Mechs/{unit_name}"
    else:
        unit_path = f"/Game/NeonGrid/Kaiju/{unit_name}"

    unit_asset = unreal.EditorAssetLibrary.load_asset(unit_path)
    if not unit_asset:
        return None

    editor_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    world = editor_subsystem.get_editor_world()
    if not world:
        return None

    # Place slightly above the ground
    world_pos = unreal.Vector(world_pos.x, world_pos.y, world_pos.z + 10)

    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.SkeletalMeshActor,
        world_pos,
        unreal.Rotator(0, ISO_YAW, 0)
    )
    if actor:
        actor.skeletal_mesh_component.set_skinned_asset_and_update(unit_asset)
        actor.set_actor_label(f"Unit_{faction}_{x}_{y}_{unit_name}")
        return actor
    return None
```

## Import Options: Convert Scene & Uniform Scale

Two critical import settings verified in NeonGrid:

| Setting | Value | Why |
|---|---|---|
| `convert_scene` | `True` | Fixes coordinate system mismatch (GLB is +Y-up, UE is +Z-up) |
| `import_uniform_scale` | `1.0` | GLB units are already in centimeters (matching UE) |
| `import_materials` | `False` | Materials handled separately in NeonGrid pipeline |
| `import_textures` | `False` | Textures handled separately |

**Note**: These are set via `ui.static_mesh_import_data.set_editor_property()` and `ui.skeletal_mesh_import_data.set_editor_property()` — NOT via `FbxAssetImportOptions`.

## Running Python Scripts in UE 5.8

```bash
# From command line (headless)
UnrealEditor-Cmd.exe <uproject> -run=PythonScript -script=import_neongrid.py -log

# From UE Python console
import import_neongrid
import_neongrid.main()

# With arguments
UnrealEditor-Cmd.exe <uproject> -run=PythonScript -script=import_neongrid.py -log
```

## Common Gotchas

1. **`SupportedClasses` requirement**: In UE 5.8, `UAssetActionUtility` and `UActorActionUtility` require `SupportedClasses` to be set (empty = data validation error).
2. **Packed return values**: Python functions returning multiple values must pack in declared order: `return (10, "hello")` not `("hello", 10)`.
3. **GLB coordinate system**: GLB uses +Y-up, UE uses +Z-up. `convert_scene` must be enabled.
4. **Skeletal mesh auto-rig**: UE 5.8 can auto-create skeletons from GLB, but the rig may need cleanup in the Control Rig editor.
5. **Asset naming**: Use consistent naming (e.g., `SM_Mech_Assault`, `SK_Kaiju_Titanosaurus`, `WPN_IronSword`) for easy lookup.
6. **`spawn_actor_from_class`**: Use `unreal.EditorLevelLibrary.spawn_actor_from_class()` — NOT `level.spawn_actor()` or `editor_level_lib.spawn_actor()`.
7. **Editor subsystem**: Access the world via `unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)` — NOT via `level` parameter.
8. **Isometric projection**: Use proper isometric math: `world_x = (x - y) * GRID_SIZE * 0.866`, `world_y = (x + y) * GRID_SIZE * 0.5`.

## Related

- ← Previous: [[13_Importing_Assets]]
- → Next: [[14_Importing_Character_Animation]]
- 📚 Series: [[_MOC_UE5_7_Starter_Course]]
- 📚 See also: [[UE58_API_Changes]] (Scripting section)
