# Ravindra K R

Platform engineer across DevOps, MLOps and AIOps. I run Kubernetes for a robot fleet, the CI and GPU platform behind it, and the ML training and inference pipelines on top, and I fix what breaks along the way in the open-source tools we depend on.

**Golden Kubestronaut** (every CNCF and Linux Foundation cloud-native certification) · Terraform Associate · LFCS

## Upstream contributions

Bugs found while operating these projects in production, fixed with a regression test, and merged upstream.

| Project | Change | Status |
|---|---|---|
| [cert-manager](https://github.com/cert-manager/cert-manager/pull/9303) | certificate-shim no longer mutates the informer cache's labels; backported to [1.21](https://github.com/cert-manager/cert-manager/pull/9314) and [1.20](https://github.com/cert-manager/cert-manager/pull/9315) at the maintainers' request | merged |
| [rclnodejs](https://github.com/RobotWebTools/rclnodejs/pull/1595) | interrupted ROS 2 message generation no longer leaves a partial `generated/` tree that `init()` treats as complete | merged |

Open work in review across Argo CD, Kueue, Tempo, external-secrets, actions-runner-controller, aws-load-balancer-controller and others: [all pull requests](https://github.com/pulls?q=is%3Apr+author%3AKR-Ravindra+archived%3Afalse+sort%3Aupdated-desc) · [issues filed](https://github.com/issues?q=is%3Aissue+author%3AKR-Ravindra+archived%3Afalse+sort%3Acreated-desc)

## What I work on

- **Kubernetes at the edge**: a fleet of robots running k3s, managed with Argo CD, Tailscale and Kyverno; observability with Prometheus, Loki and Tempo.
- **MLOps on EKS**: GPU batch and distributed training with Kueue, MultiKueue and Slurm on Kubernetes; Argo Workflows for data and inference pipelines; MLflow for experiment tracking; Karpenter spot capacity for GPUs; KubeRay pilots.
- **CI platform**: GitHub Actions runners on EKS with Karpenter, container build caches and registries, benchmark and GPU test suites.
- **AIOps**: LLM agents wired into the operations loop, from incident triage against Prometheus, Loki and Tempo to unattended code changes behind mechanical gates.
- **Self-hosted coding agents**: an open-weight model served with vLLM, a plugin-based agent harness, and a nine-check gate between the model and `git push`. Write-up coming.

## Certifications

CKA · CKAD · CKS · KCNA · KCSA · PCA · OTCA · ICA · CCA · CAPA · CGOA · CBA · KCA · HashiCorp Terraform Associate · LFCS

## Elsewhere

[mutate-me](https://github.com/KR-Ravindra/mutate-me), a Kubernetes mutating admission webhook in Go · [helm-charts](https://github.com/KR-Ravindra/helm-charts) · [civic-guardian](https://github.com/KR-Ravindra/civic-guardian)

<img src="github-metrics.svg" alt="GitHub activity" width="100%">
