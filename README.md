# CODEX CAELI — Blender / MPFB2

15-second vertical 3D character-animation test based on the Selena storyline. This repository is intended to produce an **actual skinned MakeHuman/MPFB2 character inside Blender**, not a geometric stand-in.

The automation is designed to fetch Blender, [MPFB2](https://github.com/makehumancommunity/mpfb2) and original [MakeHuman System Assets (CC0)](https://static.makehumancommunity.org/assets/assetpacks/makehuman_system_assets.html), create an editable .blend scene, render a portrait MP4 with CPU on GitHub Actions, and upload the outputs as workflow artifacts.

It uses a real human mesh, armature animation, original wardrobe/hair/eyes assets, a dim archive set, key lights, and a moving cinematic camera.

The first test is **15 seconds / 12 fps / 360×640**. It is a feasibility render, not a guaranteed match for the reference's high-end stylized 3D. Full-quality rendering requires later refinement.

## Render
Open the **Actions** tab and select **Render real Blender MPFB2 character**. A successful run publishes **codex-caeli-real-mpfb2-render** under Artifacts; that ZIP contains MP4 and Blender .blend. External model mirrors and CPU-runner render time can cause the workflow to fail; do not claim a successful video until GitHub reports success.

No paid asset, stolen artwork, or commercial audio is bundled. The script and build steps are project-specific; upstream dependencies retain their original licenses.