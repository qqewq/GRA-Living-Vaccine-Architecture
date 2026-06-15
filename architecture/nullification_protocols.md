# Nullification Protocols

## Hard Nullification
- **Trigger**: Any stability violation (activation > max, energy <= 0, toxicity > threshold).
- **Action**: Immediate removal from simulation.
- **Use case**: Maximum safety, irreversible conditions.

## Soft Nullification
- **Trigger**: Same as hard, but configured via policy.
- **Action**: Agent deactivates (activation = 0) but remains in simulation. Can recover if signals improve.
- **Use case**: Temporary adverse conditions, recoverable toxicity.

## Love-Oriented Nullification
- **Trigger**: Stability violation with love policy enabled.
- **Action**: Before removal, agent distributes `transfer_fraction` of its energy to nearest neighbors and emits a love signal.
- **Use case**: Swarm resilience, preventing population collapse.

## Configuration

In `stability` section of agent YAML:
```yaml
stability:
  max_activation_level: 1.0
  nullification_policy:
    type: love_oriented  # hard | soft | love_oriented
    transfer_fraction: 0.8
```
