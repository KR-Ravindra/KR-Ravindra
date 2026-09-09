# Ravindra K R

**DevOps · MLOps · AIOps platform engineer.** I run Kubernetes for a fleet of robots, the CI and GPU platform behind it, and the ML training and inference pipelines on top, and I fix what breaks along the way in the open-source tools we depend on.

**Golden Kubestronaut** (every CNCF and Linux Foundation cloud-native certification) 

## Upstream contributions

Bugs found while operating these projects in production, fixed with a regression test, and merged upstream.

| Project | Change | Status |
|---|---|---|
| [Kubernetes security-profiles-operator](https://github.com/kubernetes-sigs/security-profiles-operator/pull/3422) | operator and webhook run as non-root with all Linux capabilities dropped, with a render test that pins it | merged |
| [cert-manager](https://github.com/cert-manager/cert-manager/pull/9303) | certificate-shim no longer mutates the informer cache's labels; backported to [1.21](https://github.com/cert-manager/cert-manager/pull/9314) and [1.20](https://github.com/cert-manager/cert-manager/pull/9315) at the maintainers' request | merged |
| [actions-runner-controller](https://github.com/actions/actions-runner-controller/pull/4626) | default and per-controller `max-concurrent-reconciles` flags for the GitHub Actions runner controller | merged |
| [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox/pull/890) | ROS 2 Humble backport of the `save_map` name validation that closed a shell-injection path | merged |
| [rclnodejs](https://github.com/RobotWebTools/rclnodejs/pull/1595) | interrupted ROS 2 message generation no longer leaves a partial `generated/` tree that `init()` treats as complete | merged |
| [goreleaser](https://github.com/goreleaser/goreleaser/pull/7127) | git tag parsing no longer breaks when the user's gitconfig sets `column.ui` | merged |

Open work in review across Kubernetes, Argo CD, Kueue, Tempo, linkerd, Harbor, kops, aws-load-balancer-controller and others: [all pull requests](https://github.com/pulls?q=is%3Apr+author%3AKR-Ravindra+archived%3Afalse+sort%3Aupdated-desc) · [issues filed](https://github.com/issues?q=is%3Aissue+author%3AKR-Ravindra+archived%3Afalse+sort%3Acreated-desc)

## What I work on

- **MLOps on EKS**: GPU batch and distributed training with Kueue, MultiKueue and Slurm on Kubernetes; Argo Workflows for data and inference pipelines; MLflow for experiment tracking; Karpenter spot capacity for GPUs; KubeRay pilots.
- **CI platform**: GitHub Actions runners on EKS with Karpenter, container build caches and registries, benchmark and GPU test suites.
- **AIOps**: LLM agents in the operations loop, from incident triage against Prometheus, Loki and Tempo to code changes that only land after mechanical checks.

More on [Credly](https://www.credly.com/users/kathi-raja-ravindra/badges).
