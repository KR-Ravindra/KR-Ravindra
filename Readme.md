# Ravindra K R

**DevOps · MLOps · AIOps platform engineer.** I run Kubernetes for a fleet of robots, the CI and GPU platform behind it, and the ML training and inference pipelines on top, and I fix what breaks along the way in the open-source tools we depend on.

**Golden Kubestronaut** (every CNCF and Linux Foundation cloud-native certification) 

## Upstream contributions

Bugs found while operating these projects in production, fixed with a regression test, and merged upstream.

| Project | Change | Status |
|---|---|---|
| [cert-manager](https://github.com/cert-manager/cert-manager/pull/9303) | certificate-shim no longer mutates the informer cache's labels; backported to [1.21](https://github.com/cert-manager/cert-manager/pull/9314) and [1.20](https://github.com/cert-manager/cert-manager/pull/9315) at the maintainers' request | merged |
| [rclnodejs](https://github.com/RobotWebTools/rclnodejs/pull/1595) | interrupted ROS 2 message generation no longer leaves a partial `generated/` tree that `init()` treats as complete | merged |

Open work in review across Argo CD, Kueue, Tempo, external-secrets, actions-runner-controller, aws-load-balancer-controller and others: [all pull requests](https://github.com/pulls?q=is%3Apr+author%3AKR-Ravindra+archived%3Afalse+sort%3Aupdated-desc) · [issues filed](https://github.com/issues?q=is%3Aissue+author%3AKR-Ravindra+archived%3Afalse+sort%3Acreated-desc)

## What I work on

- **MLOps on EKS**: GPU batch and distributed training with Kueue, MultiKueue and Slurm on Kubernetes; Argo Workflows for data and inference pipelines; MLflow for experiment tracking; Karpenter spot capacity for GPUs; KubeRay pilots.
- **CI platform**: GitHub Actions runners on EKS with Karpenter, container build caches and registries, benchmark and GPU test suites.
- **AIOps**: LLM agents in the operations loop, from incident triage against Prometheus, Loki and Tempo to code changes that only land after mechanical checks.

## Certifications

All verifiable on [Credly](https://www.credly.com/users/kathi-raja-ravindra/badges).

- **Linux Foundation / CNCF**: CNPE (Certified Cloud Native Platform Engineer), CNPA, CKA, CKAD, CKS, KCNA, KCSA, PCA, OTCA, ICA, CCA, CAPA, CGOA, CBA, KCA, LFCS. Golden Kubestronaut, April 2025.
- **AWS**: Solutions Architect Associate, Developer Associate, Cloud Practitioner.
- **HashiCorp**: Terraform Associate (003).
- **Isovalent**: Lab Champion (30 labs) across Cilium, Hubble, Tetragon and eBPF.
