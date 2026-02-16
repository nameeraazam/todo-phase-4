# Tasks: Helm Chart for Todo Chatbot

**Input**: Design documents from `/specs/002-helm-chart-todo-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Helm Chart**: `helm-chart/` at repository root
- **Kubernetes Templates**: `helm-chart/templates/`
- **Configuration**: `helm-chart/values.yaml`
- **Chart Metadata**: `helm-chart/Chart.yaml`
- **Helper Templates**: `helm-chart/templates/_helpers.tpl`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create helm-chart directory structure
- [X] T002 Initialize Chart.yaml with metadata for todo-chatbot chart
- [X] T003 [P] Create initial values.yaml with default configurations
- [X] T004 [P] Create README.md for the Helm chart

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create _helpers.tpl with common label templates
- [X] T006 [P] Create namespace configuration (todo-app)
- [X] T007 Set up security context configurations with runAsNonRoot
- [X] T008 [P] Configure global values structure in values.yaml
- [X] T009 [P] Set up common labels and selectors for all resources

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Deploy Todo Chatbot Application (Priority: P1) 🎯 MVP

**Goal**: Deploy the Todo Chatbot application using a Helm chart with both frontend and backend components running in Kubernetes.

**Independent Test**: Can be fully tested by installing the Helm chart in a Kubernetes cluster and verifying that both frontend and backend pods are running and accessible.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [X] T010 [P] [US1] Helm lint validation test for chart in tests/helm-lint-test.sh
- [X] T011 [P] [US1] Kubernetes manifest validation test in tests/k8s-validation-test.sh

### Implementation for User Story 1

- [X] T012 [P] [US1] Create frontend deployment template in helm-chart/templates/deployment-frontend.yaml
- [X] T013 [P] [US1] Create backend deployment template in helm-chart/templates/deployment-backend.yaml
- [X] T014 [P] [US1] Create frontend service template in helm-chart/templates/service-frontend.yaml
- [X] T015 [P] [US1] Create backend service template in helm-chart/templates/service-backend.yaml
- [X] T016 [US1] Configure frontend deployment with proper resource limits and probes
- [X] T017 [US1] Configure backend deployment with proper resource limits and probes
- [X] T018 [US1] Configure frontend service as LoadBalancer type
- [X] T019 [US1] Configure backend service as ClusterIP type
- [X] T020 [US1] Set up environment variables for frontend to connect to backend service
- [X] T021 [US1] Verify both deployments can be installed and pods are running

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Configure Application Settings (Priority: P2)

**Goal**: Allow customization of application settings through values.yaml so that configurations like image tags, resource limits, and replica counts can be adjusted without modifying chart templates.

**Independent Test**: Can be tested by deploying the chart with custom values and verifying that the deployed resources reflect the custom settings.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T022 [P] [US2] Test custom values override defaults in tests/values-override-test.sh
- [X] T023 [P] [US2] Test upgrade with new values in tests/upgrade-values-test.sh

### Implementation for User Story 2

- [X] T024 [P] [US2] Configure frontend replica count as configurable value in values.yaml
- [X] T025 [P] [US2] Configure backend replica count as configurable value in values.yaml
- [X] T026 [P] [US2] Configure image repository and tag as configurable values in values.yaml
- [X] T027 [P] [US2] Configure resource requests and limits as configurable values in values.yaml
- [X] T028 [P] [US2] Configure service types as configurable values in values.yaml
- [X] T029 [US2] Configure probe settings as configurable values in values.yaml
- [X] T030 [US2] Configure environment variables as configurable values in values.yaml
- [X] T031 [US2] Test that custom values properly override default configurations
- [X] T032 [US2] Verify upgrade functionality with new values

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Scale Application Components (Priority: P3)

**Goal**: Enable independent scaling of frontend and backend components so that resource utilization can be optimized based on demand.

**Independent Test**: Can be tested by adjusting replica counts in values.yaml and verifying that the deployments scale accordingly.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T033 [P] [US3] Test frontend scaling functionality in tests/frontend-scaling-test.sh
- [X] T034 [P] [US3] Test backend scaling functionality in tests/backend-scaling-test.sh

### Implementation for User Story 3

- [X] T035 [P] [US3] Verify frontend deployment scales correctly with replica count changes
- [X] T036 [P] [US3] Verify backend deployment scales correctly with replica count changes
- [X] T037 [US3] Test that scaling doesn't affect service connectivity
- [X] T038 [US3] Document scaling procedures in README.md
- [X] T039 [US3] Verify that scaled components maintain proper resource limits
- [X] T040 [US3] Test load distribution across multiple frontend replicas

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T041 [P] Documentation updates in helm-chart/README.md
- [X] T042 Code cleanup and refactoring of Helm templates
- [X] T043 Performance optimization across all deployments
- [X] T044 [P] Additional unit tests for Helm chart in tests/
- [X] T045 Security hardening of all deployments
- [X] T046 Run quickstart.md validation to ensure installation works as documented
- [X] T047 [P] Add NOTES.txt template for post-installation instructions
- [X] T048 Create sample custom-values.yaml file for documentation
- [X] T049 Validate chart against Kubernetes best practices

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds upon US1 configurations
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Builds upon US1/US2 configurations

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Templates before configurations
- Core implementations before integrations
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all templates for User Story 1 together:
Task: "Create frontend deployment template in helm-chart/templates/deployment-frontend.yaml"
Task: "Create backend deployment template in helm-chart/templates/deployment-backend.yaml"
Task: "Create frontend service template in helm-chart/templates/service-frontend.yaml"
Task: "Create backend service template in helm-chart/templates/service-backend.yaml"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Constitution Compliance Tasks

### Statelessness Requirement
- [X] T050 Ensure all data is persisted externally, no in-memory storage in pods
- [X] T051 Verify system survives pod restarts and scales horizontally

### MCP Tool Compliance
- [X] T052 Implement all task operations exclusively through MCP tools
- [X] T053 Prohibit direct Kubernetes operations outside MCP tools
- [X] T054 Validate all tool calls follow MCP specification exactly

### Natural Language Interface
- [X] T055 Ensure backend API supports AI-driven natural language processing
- [X] T056 Verify interface handles various user expression methods

### Conversation Persistence
- [X] T057 Verify all conversation history is stored externally with unique conversation_id
- [X] T058 Ensure AI agent can resume conversations from any point

### Containerization Standards
- [X] T059 Verify frontend uses Node 20-alpine base image as per research.md
- [X] T060 Verify backend uses Python 3.11-slim base image as per research.md
- [X] T061 Implement health checks for both services as per contracts
- [X] T062 Optimize container images for size and security
- [X] T069 Create Dockerfile for frontend application
- [X] T070 Create Dockerfile for backend application

### Kubernetes Deployment
- [X] T063 Verify Helm chart follows Kubernetes best practices
- [X] T064 Configure resource requests and limits as per spec.md
- [X] T065 Set up liveness and readiness probes as per spec.md
- [X] T066 Configure service discovery between frontend and backend using internal DNS
- [X] T067 Implement security contexts with runAsNonRoot as per research.md
- [X] T068 Ensure chart passes all Helm linting and Kubernetes validation checks