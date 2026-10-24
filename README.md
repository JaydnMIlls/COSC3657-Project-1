# COSC 3657 Unit 1: Bare-Metal IPC & Custom Protocol Design

**Student:** Jaydn Mills

## Deliverables Checklist
- [x] Complete implementation of `protocol.py` handling partial socket reads (`recv_exact`).
- [x] Complete implementation of `storage.py` wrapped in explicit `threading.Lock` and `threading.Condition` primitives.
- [x] Complete implementation of `server.py` utilizing `concurrent.futures.ThreadPoolExecutor`.
- [x] Terminal screenshot proving all 20 worker threads in `client_stress_test.py` execute without race condition failures or unhandled socket exceptions.

## Verification Screenshot
![Listening Verification<img width="1212" height="300" alt="Screenshot 2026-10-23 223445" src="https://github.com/user-attachments/assets/55399718-992c-4788-9df2-82deb3817ca9" />
]()
![Stress Test Verification](<img width="1208" height="473" alt="Screenshot 2026-10-23 223510" src="https://github.com/user-attachments/assets/6e563989-d99f-4d1c-8257-3648145d0b04" />
)
![Server Side Logs<img width="1210" height="804" alt="Screenshot 2026-10-23 223521" src="https://github.com/user-attachments/assets/e18c5e5a-8845-4ec4-b2eb-3ba69b56cb10" />
]()
