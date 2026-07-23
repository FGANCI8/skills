---
name: renova-aura-android-kotlin-engineering
description: Design, audit and implement Android-native Kotlin applications with Jetpack Compose, lifecycle-safe state, offline and sync contracts, secure storage, accessibility and testable architecture. Use only for real Android/Kotlin modules or an approved native-app specification.
---

# Renova Aura Android Kotlin Engineering

## Mission

Produce maintainable Android-native behavior without treating a web preview as the application.

## Activate when

- Gradle/Kotlin/Android modules exist;
- a Compose screen, navigation, repository, Room, WorkManager or Android permission is involved;
- a web prototype must be translated into a native implementation plan.

## Sources

Read Gradle/version catalog, manifest, modules, navigation, Compose UI, state holders, use cases, repositories, network, storage, workers, permissions and tests.

## Procedure

1. Confirm Android project root, variants and installed versions.
2. Map UI → state → domain/use case → repository → local/remote source.
3. Verify lifecycle, process death, rotation, saved state and one-off events.
4. Define offline, synchronization, conflict and retry behavior.
5. Protect tokens/PII using platform-appropriate secure storage and least permissions.
6. Audit Compose stability, recomposition, lists, images and performance.
7. Validate TalkBack, font scaling, contrast, touch targets and keyboard/input.
8. Require unit, repository, Compose UI and instrumentation tests according to risk.

## Gates

No signing key access, Play Store publication, production backend change, real user data or destructive migration without explicit approval.

## Output

Architecture map, screen/state/data matrix, gaps, affected modules, implementation slices, tests, build commands and rollback.

## Validation

Do not claim Android completion from screenshots or web preview. Require Gradle/build evidence and device/emulator tests for implemented work.

## Rollback

Keep changes modular and reversible; preserve schema compatibility and feature-gate risky native flows.