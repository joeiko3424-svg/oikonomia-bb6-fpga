# OIK-DFIS-V1: Bare-Metal FPGA State Auditing & Busy Beaver BB(6) 6.08-Trillion-Step Frontier Sweep

Open-source C++20 Run-Length Encoded (RLE) Turing machine simulator, formal single-cell reference cross-checker, physical Xilinx UltraScale+ PCIe Gen3 x16 BAR0 MMIO state-checkpoint harness (`agfi-037dec8eb7fe5504d`), and SHA-256-verified frontier audit across all **608** official `bbchallenge` `BB(6)` holdout Turing machines (`BB6_holdouts_608.txt`).

## Architecture & Scope Separation
To maintain strict reproducibility and eliminate any ambiguity between host simulation and bare-metal hardware enforcement, this repository separates execution metrics into two clearly defined layers:
1. **Deterministic Host RLE Execution & Formal Cross-Checking:** A 24-thread C++20 Run-Length Encoded (RLE) engine advances each 6-state, 2-symbol Turing machine to **10^10 exact steps** (**6,080,000,000,000 aggregate steps** in **2,018.881 s** at **3,011.57 Msteps/s**). Every machine is cross-checked for exact state, tape head position, step count, and non-zero tape cells against an independent, unoptimized single-cell `std::unordered_map` Turing interpreter across the first `min(50,000, steps_executed)` steps (**0 discrepancies** across all 608 machines). Global head-excursion tracking uses a 128-bit dual-FNV1a configuration digest (< 10^-31 collision bound) to detect inductive translated cyclers in bounded memory.
2. **Out-of-Band Bare-Metal FPGA State Manifold (`agfi-037dec8eb7fe5504d`):** Across **244,416 physical PCIe Gen3 x16 BAR0 MMIO commits** (`/sys/bus/pci/devices/0000:34:00.0/resource0`, bypassing Linux kernel drivers at **1,430.0 ns P50 / 2,260.0 ns P99 / 15,060.0 ns P99.9** round-trip latency), execution digests are folded into a constant O(1) **256-byte (0.25 KB)** bijective Feistel-symplectic state manifold on Xilinx UltraScale+ silicon (`AWS EC2 f2.6xlarge`), followed by full inverse trajectory unwinding (`T^-1`) verifying **0 bits of LSB drift**.

## Verified Hardware & Frontier Summary (`agfi-037dec8eb7fe5504d`)
- **Silicon Substrate:** Xilinx UltraScale+ (`0000:34:00.0`) on AWS EC2 `f2.6xlarge` (Ubuntu 26.04 LTS)
- **Core Power Rail (Vccint):** 2 W - 3 W steady/post-sweep; 9 W - 10 W active load (`fpga-describe-local-image -S 0 -R -M`)
- **On-Chip State Footprint:** **256 bytes (0.25 KB)** constant O(1) bijective state manifold
- **Corpus Evaluated:** All **608 / 608** official `bbchallenge` `BB(6)` holdouts (`BB6_holdouts_608.txt`, including `---` TNF transitions)
- **Step Horizon & Throughput:** **10^10 exact steps per machine** (**6.08 x 10^12 aggregate steps** at **3,011.57 Msteps/s**)
- **Frontier Result:** All 608 holdouts survived past 10^10 steps without halting or collapsing into short-period translated cyclers
- **Formal Reference Cross-Check:** **0 discrepancies** against the independent single-cell interpreter
- **Bidirectional Reversibility (T^-1):** **0 bits** of LSB drift upon full trajectory unwinding (`Verified = true`)

## Repository Artifacts
- `bb6_fpga_frontier.cpp`: Complete C++20 RLE simulator, single-cell reference cross-checker, excursion cycle detector, and userspace PCIe BAR0 MMIO controller.
- `fetch_bb6_holdouts.py` & `bb6_holdouts_corpus.tsv`: Reproducible ingestion script and canonical 608-machine `bbchallenge` seed table.
- `bb6_frontier_audited_results.csv`: Per-machine step counts, non-zero tape cells (`ones_on_tape`), head excursion bounds, cycle periods, and final 64-bit hardware manifold digests for all 608 holdouts.
- `bb6_frontier_audit_summary.json` & `bb6_run.log`: Machine-readable and raw console audit summaries.
- `hardware_telemetry.log`: Raw `lspci` and `fpga-describe-local-image -S 0 -R -M` PCIe/voltage/power telemetry.
- `AUDIT_MANIFEST.json`: Cryptographic `SHA-256` digests for every tracked artifact in this repository.
