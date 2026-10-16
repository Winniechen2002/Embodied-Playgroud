<!-- bilingual-navigation:start -->
[English](rules_model_only.en.md) | [简体中文](rules_model_only.zh-CN.md) | [Original](rules_model_only.md) | [All documents](docs/README.en.md)
<!-- bilingual-navigation:end -->

<a id="section-1"></a>
# Level 0: Code-enabled control without prebuilt domain tools

Current catalog tasks use cold-start attempts with no cross-attempt memory or trajectory reuse. Follow the [shared rules](rules.en.md) and the declared experiment’s attempt and resource budgets.

Capability profile version: `2026-10-09-environment-l0-l3`.

Level 0 permits Python code, the standard library, NumPy and Pillow. Programs may
perform ordinary numerical computation, crop/resize images, organize actions and
implement their own dynamics prediction, inverse kinematics or motion planning.
The restriction concerns access to prebuilt domain tools, not algorithms written
by the client using these basic dependencies.

<a id="section-2"></a>
## Inputs and access

Use declared task goals and parameters, RGB images, camera calibration, public
robot information and proprioception. The current episode's Launcher spring
stiffness in N/m is public. Hidden poses, geometry, contacts, reset seeds and
private scoring diagnostics are not Level 0 inputs. Generated code does not grant
access to simulator source, assets, private files or native handles.

<a id="section-3"></a>
## Unavailable tools

Do not invoke prebuilt dynamics/simulator, IK or motion-planning tools or domain
libraries. External depth, segmentation, reconstruction, tracking, grasp/contact
models and additional pretrained action-policy tools are unavailable. Level 0
has no gateway tool grants. Basic numerical and image-processing libraries and
a client's own algorithms remain permitted; public robot data may be used.

<a id="section-4"></a>
## Environment boundary

Only declared robot actions advance the environment. No reset, teleport, direct
state write, configuration change or scoring override is a client capability.
The environment's native servo, action scaling and explicitly declared fixtures
are part of the environment. The gateway never silently solves IK or repairs an
action on behalf of the client. Invalid actions are rejected.

Code may store and replay its own permitted observations and actions. Higher-level
privileged traces or prebuilt controllers do not become Level 0 inputs by copying
them into a file. Existing physical task rules continue to apply.

<a id="section-5"></a>
## Version and scope

Record `capability_level: 0` and the capability version above separately from
observation profile and task difficulty. The gateway enforces its own field,
resource and tool authorization; it cannot certify libraries used by an arbitrary
external Python client. This environment release does not implement model token
or image-read accounting and does not publish model evaluation results. Experiment
hosts may apply separate budgets; this does not change environment permissions.
Historical profiles retain their original version and are not relabelled.
