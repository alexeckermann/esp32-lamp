# TODO

- [x] Build a prototype board with power supply
- [ ] Evaluating MicroPython for performance and capability
  - Animation speed, smoothness, complexity
  - Concurrent tasks (animation & control)
- [ ] Testing animations and driving LED strip

---

## Performance and stability testing

Test directory: `./test/neopixel-test`

- How fast can an animation tick?
- Are there any performance impacts?
- Stable animation?
- Best way to store animations?
  - Precompiling the data and storing in a list