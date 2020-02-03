-- Resource: https://github.com/timotta/wrk-scripts/blob/master/multiplepaths.lua

-- Initialize the pseudo random number generator
-- Resource: http://lua-users.org/wiki/MathLibraryTutorial
math.randomseed(os.time())
math.random(); math.random(); math.random()

fname="pathResult"

-- Shuffle array
-- Returns a randomly shuffled array
function shuffle(paths)
  local j, k
  local n = #paths

  for i = 1, n do
    j, k = math.random(n), math.random(n)
    paths[j], paths[k] = paths[k], paths[j]
  end

  return paths
end

-- Load URL paths from the file
function load_url_paths_from_file(file)
  lines = {}

  -- Check if the file exists
  -- Resource: http://stackoverflow.com/a/4991602/325852
  local f=io.open(file,"r")
  if f~=nil then 
    io.close(f)
  else
    -- Return the empty array
    return lines
  end

  -- If the file exists loop through all its lines 
  -- and add them into the lines array
  for line in io.lines(file) do
    if not (line == '' or line == nul) then
      lines[#lines + 1] = line
    end
  end

  return shuffle(lines)
end

clone = function(t) 
    l = {}
    for k,v in pairs(t) do
        l[k] = v
    end
    return l
end
-- Load URL paths from file
paths = load_url_paths_from_file(fname)
heap = {}
-- Check if at least one path was found in the file
if #paths <= 0 then
  print("multiplepaths: No paths found. You have to create a file " .. fname .. " with one path per line")
  os.exit()
end
current=1
print("multiplepaths: Found " .. #paths .. " paths")

-- Initialize the paths array iterator

request = function()
  -- Get the next paths array element
  if #heap == 0 then
      table.insert(heap,paths[current])
      current = current+1
      if current == #paths + 1 then
          current = 1
       end
  end

  url_path = heap[#heap]
  table.remove(heap, #heap)

  -- Return the request object with the current URL path
  return wrk.format(nil, url_path), url_path
end

function response(status,headers,body,user)
    table.insert(table,user)
end
