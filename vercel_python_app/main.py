
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for external access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Student marks database
student_marks = {"0": 45, "i1": 34, "XpnuGx": 54, "yr58": 72, "jVeR1q": 93, "FDWMOGH": 2, "sPYJR": 90, "N": 60, "g": 81, "IsvFkhW1wW": 54, "Sn6": 92, "rI": 33, "i": 47, "89fPECdQr": 64, "fvZ4iMFG": 77, "GNdj4ytZ": 13, "vv6fLc0QW": 33, "4IT50Vm8": 52, "66VfQO": 52, "hzQ": 63, "f0mqqC": 82, "mwUQuTm": 31, "ploi8pQL0B": 81, "jd8X6EpJn": 1, "GVOp": 57, "DY5f4sm": 24, "capF0S7n": 8, "XaRYyfy": 41, "BUBcH": 54, "ePiR9": 59, "I2zkg": 11, "p14HZ8": 92, "fxm6cp2": 44, "gkSupzH": 72, "WzGqr1z": 40, "k": 89, "1upz": 68, "AZ286": 9, "j1HAP": 89, "9lC9": 90, "e0SRdCPeEj": 62, "yvOY8": 25, "eIKDKP31s": 83, "cml0Evv": 70, "FIyEB": 57, "yRiRgFsb": 28, "sW8nQJrm": 87, "mNj8iD": 87, "tookvVp": 47, "aAZ": 43, "7fisUQ2": 43, "bHG": 22, "Ws4": 23, "ZeHGRru3Vi": 42, "rqOIo7a": 71, "4bWd": 33, "LF": 74, "7VsPlBwz": 28, "jnfLWfE8D9": 20, "03h": 50, "0xjsrxHOH": 69, "WHy4uC": 29, "sD": 92, "m89hD2kQXy": 88, "z631Q1KSB": 15, "77V": 81, "SJ": 15, "vuxcKpOUR": 13, "YLns": 27, "W": 9, "WE": 47, "hcLD": 87, "3ukT2HS": 4, "MnbXHAyAQp": 4, "rZc": 87, "Eh9": 8, "tBaNSRsx": 46, "uL7prt": 94, "zq": 13, "PFv0bWi": 89, "nZv0gsVR": 19, "VQyDp": 19, "MyAV": 76, "8xo0GJB": 65, "KxITK5X1z": 78, "Raonhc": 97, "8sbDfy0": 6, "r2": 95, "6J2H4k1E": 81, "Y2aTV0ur": 30, "H": 61, "jr": 73, "4": 33, "dyo": 58, "vI": 93, "c2juJZu6R": 80, "wnP": 89, "y": 83, "RXDIqxxiwh": 81, "M6ZF": 15}

@app.get("/")
async def root():
    return {"message": "API is working. Try /api?name=John"}

@app.get("/api/")
async def get_marks(name: list[str] = Query(...)):
    marks = [student_marks.get(n, None) for n in name]
    return {"marks": marks}
