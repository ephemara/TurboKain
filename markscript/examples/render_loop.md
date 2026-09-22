# RenderEngine

The render domain owns the frame pipeline. Each routine maps to a phase
in the render loop - setup, draw, present.

## setup_frame

> allocate command buffer
> reset descriptor pools
| Pool | Frame Allocator | Dynamic |

## draw_scene

> bind vertex buffers
> issue draw calls
> resolve MSAA targets
| Samples | 4x | Adaptive |

## present_frame

> signal semaphore
> queue submit
> present swapchain
| VSync | True | Mailbox |
