# NeuralCompute

This domain defines a multi-stage neural compute pipeline using
MarkScript intents to orchestrate GPU kernel dispatches.

## init_weights

> allocate weight buffer
> initialize with Xavier uniform
> copy to device memory
| Precision | FP16 | Tensor Core |
| Dimensions | 4096x2048 | Row Major |

## forward_pass

> dispatch matmul kernel
> apply ReLU activation
> run batch normalization
| BatchSize | 256 | Warp |
| Activation | ReLU | Inline |

## backward_pass

> compute loss gradient
> dispatch backprop kernel
> update weights via Adam
| LearningRate | 0.001 | Adaptive |
| Beta1        | 0.9   | Default  |
| Beta2        | 0.999 | Default  |

## checkpoint

> synchronize device
> copy weights to host
> write checkpoint file
| Path | /models/checkpoint.pt | Overwrite |
