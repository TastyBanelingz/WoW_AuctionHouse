function wait(seconds)
    local start = os.time()
    repeat until os.time() > start + seconds
  end

function string:split(sSeparator, nMax, bRegexp)
    assert(sSeparator ~= '')
    assert(nMax == nil or nMax >= 1)
 
    local aRecord = {}
 
    if self:len() > 0 then
       local bPlain = not bRegexp
       nMax = nMax or -1
 
       local nField, nStart = 1, 1
       local nFirst,nLast = self:find(sSeparator, nStart, bPlain)
       while nFirst and nMax ~= 0 do
          aRecord[nField] = self:sub(nStart, nFirst-1)
          nField = nField+1
          nStart = nLast+1
          nFirst,nLast = self:find(sSeparator, nStart, bPlain)
          nMax = nMax-1
       end
       aRecord[nField] = self:sub(nStart)
    end
 
    return aRecord
 end

function tablelength(T)
    local count = 0
    for _ in pairs(T) do count = count + 1 end
    return count
  end


function scandir(directory)
    local i, t, popen = 0, {}, io.popen
    local pfile = popen('ls -a "'..directory..'"')
    for filename in pfile:lines() do
        i = i + 1
        if string.find(filename, "ScanData") then
            t[i] = filename
            --print(filename)
        end
    end
    pfile:close()
    return t
end


function processData(filename)
    dofile("./Data/"..filename)
    --print(AucScanData['scans']['Rattlegore']['ropes'][1])
    local keyset = {}
    local n = 0
    

    file = io.open('Data/Temp/RawData.txt', 'a');
    io.output(file);

    for k,v in pairs(AucScanData['scans']['Rattlegore']['ropes']) do
        n=n+1
        keyset[n]=k
        --print(AucScanData['scans']['Rattlegore']['ropes'][k]..','..filename)
        for k,v in next, string.split(AucScanData['scans']['Rattlegore']['ropes'][k], "},{") 
            do 
            io.write(v..','..filename..'\n')
        end
    end

    io.close(file);

    return nil
end

files = scandir("./Data")

len = tablelength(files)

file = io.open('RawData.txt', 'w');
io.output(file);
io.close(file);

mod = 4

for filename = mod, len+(mod-1) do
    print (files[filename])
    processData(files[filename])
    os.rename("./Data/"..files[filename], "./Data/Archive/"..files[filename])
end


