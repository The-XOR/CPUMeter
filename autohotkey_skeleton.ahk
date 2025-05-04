# skeletrun da inserire come base per una piu' ampia configurazione, NOI sappiamo di cosa parliamo... :-)

class COMPORT
{
    Handle = -1
    __New()
    {
        Handle = -1
        return this
    }

    __Delete()
    {
        Close()
    }

    IsOpen()
    {
        return Handle >= 0
    }

    Open(numCom)
    {
        if(!IsOpen())
        {
            h := DllCall("CreateFile"
                , "Str", port
                , "UInt", 0xC0000000  ; GENERIC_READ | GENERIC_WRITE
                , "UInt", 0           ; Exclusive access
                , "UInt", 0           ; No security attributes
                , "UInt", 3           ; OPEN_EXISTING
                , "UInt", 0           ; No overlapped I/O
                , "UInt", 0           ; No template file
                , "UPtr")             ; Return handle
                
            if(h >= 0)
            {
                VarSetCapacity(dcb, 28, 0)  ; DCB structure
                NumPut(28, dcb, 0, "UInt")  ; Structure size
                DllCall("GetCommState", "UPtr", h, "UPtr", &dcb)
                NumPut(115200, dcb, 4, "UInt")  ; Baud rate = 115200
                NumPut(8, dcb, 11, "UChar")     ; ByteSize = 8
                NumPut(0, dcb, 12, "UChar")     ; Parity = 0 (NOPARITY)
                NumPut(0, dcb, 14, "UChar")     ; StopBits = 0 (ONESTOPBIT)
                DllCall("SetCommState", "UPtr", h, "UPtr", &dcb)
                Handle = h
            }

            return h >= 0
        }

        return False
    }

    Close()
    {
        if(IsOpen())
        {
            DllCall("CloseHandle", "UPtr", Handle)
            Handle = -1
        }
    }

    Send(b)
    {
        if(IsOpen())
        {
            VarSetCapacity(byteBuf, 1, 0)
            NumPut(b, byteBuf, 0, "UChar")
            VarSetCapacity(bytesWritten, 4, 0)
            result := DllCall("WriteFile"
                , "UPtr", Handle
                , "UPtr", &byteBuf
                , "UInt", 1           ; Number of bytes to write
                , "UPtr", &bytesWritten
                , "UInt", 0           ; No overlapped I/O
                , "UInt")
            return result && bytesWritten == 1
        }

        return False
    }
}

# init:
serial = New COMPORT()
serial.Open(comPort);
SetTimer, UpdateCPULoad, -1000
    
UpdateCPULoad:
    if(serial.IsOpen())
        serial.Send(CPULoad())
    SetTimer, UpdateCPULoad, 1000
return

CPULoad()
{
    static PIT, PKT, PUT
    if (Pit = "")
    {
        return 0, DllCall("GetSystemTimes", "Int64P", PIT, "Int64P", PKT, "Int64P", PUT)
    }
    DllCall("GetSystemTimes", "Int64P", CIT, "Int64P", CKT, "Int64P", CUT)
    IdleTime := PIT - CIT, KernelTime := PKT - CKT, UserTime := PUT - CUT
    SystemTime := KernelTime + UserTime 
    return ((SystemTime - IdleTime) * 100) // SystemTime, PIT := CIT, PKT := CKT, PUT := CUT 
}
