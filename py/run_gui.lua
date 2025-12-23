script_name        = "Py Effector FX"
script_description = "Generador de efectos karaoke"
script_author      = "py-effector-fx"
script_version     = "3.0"

local PYTHON = "/Library/Frameworks/Python.framework/Versions/3.13/bin/python3"
local SCRIPT_DIR = "/Users/macbookpro/py-effector-fx/py"
local GUI_SCRIPT = SCRIPT_DIR .. "/gui_script.py"
local PROCESS_SCRIPT = SCRIPT_DIR .. "/process_effect.py"
local TEMP_FILE = "/tmp/aegisub_current.ass"
local RESULT_FILE = "/tmp/aegisub_effect_result.txt"
local LINES_FILE = "/tmp/aegisub_effect_lines.txt"

function ass_time(ms)
    local s = ms / 1000
    local cs = math.floor((ms % 1000) / 10)
    local sec = math.floor(s) % 60
    local min = math.floor(s / 60) % 60
    local hour = math.floor(s / 3600)
    return string.format("%d:%02d:%02d.%02d", hour, min, sec, cs)
end

function parse_time(time_str)
    local h, m, s, cs = time_str:match("(%d+):(%d+):(%d+)%.(%d+)")
    if not h then return 0 end
    return (tonumber(h) * 3600 + tonumber(m) * 60 + tonumber(s)) * 1000 + tonumber(cs) * 10
end

function run_effector(subs, sel, act)
    local file = io.open(TEMP_FILE, "w")
    if not file then return end
    
    file:write("[Script Info]\nScriptType: v4.00+\n\n")
    file:write("[V4+ Styles]\n")
    file:write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
    
    for i = 1, #subs do
        local line = subs[i]
        if line.class == "style" then
            file:write(string.format("Style: %s,%s,%d,%s,%s,%s,%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n",
                line.name, line.fontname, line.fontsize,
                line.color1, line.color2, line.color3, line.color4,
                line.bold and 1 or 0, line.italic and 1 or 0,
                line.underline and 1 or 0, line.strikeout and 1 or 0,
                line.scale_x, line.scale_y, line.spacing, line.angle,
                line.borderstyle, line.outline, line.shadow, line.align,
                line.margin_l, line.margin_r, line.margin_t, line.encoding))
        end
    end
    
    file:write("\n[Events]\n")
    file:write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    
    local count = 0
    for i = 1, #subs do
        local line = subs[i]
        if line.class == "dialogue" and line.effect ~= "fx" then
            file:write(string.format("Dialogue: %d,%s,%s,%s,%s,%d,%d,%d,%s,%s\n",
                line.layer, ass_time(line.start_time), ass_time(line.end_time),
                line.style, line.actor, line.margin_l, line.margin_r, line.margin_t,
                line.effect or "", line.text))
            count = count + 1
        end
    end
    file:close()
    
    os.remove(RESULT_FILE)
    os.remove(LINES_FILE)
    
    os.execute(PYTHON .. ' "' .. GUI_SCRIPT .. '" "' .. TEMP_FILE .. '"')
    
    local cf = io.open(RESULT_FILE, "r")
    if not cf then return end
    
    local config = {}
    for ln in cf:lines() do
        local k, v = ln:match("([^:]+):(.+)")
        if k and v then config[k] = v end
    end
    cf:close()
    
    local style = config.SELECTED_STYLE or ""
    
    os.execute(PYTHON .. ' "' .. PROCESS_SCRIPT .. '" "' .. TEMP_FILE .. '" "' .. RESULT_FILE .. '" "' .. LINES_FILE .. '"')
    
    local lf = io.open(LINES_FILE, "r")
    if not lf then return end
    
    local new_lines = {}
    for ls in lf:lines() do
        if ls:match("^Dialogue:") then
            local layer, st, et, sty, act, ml, mr, mv, eff, txt = 
                ls:match("Dialogue:%s*(%d+),([^,]+),([^,]+),([^,]*),([^,]*),(%d+),(%d+),(%d+),([^,]*),(.*)")
            if layer then
                table.insert(new_lines, {
                    class = "dialogue", raw = "", section = "[Events]", comment = false,
                    layer = tonumber(layer), start_time = parse_time(st), end_time = parse_time(et),
                    style = sty or style, actor = act or "", margin_l = tonumber(ml),
                    margin_r = tonumber(mr), margin_t = tonumber(mv), effect = eff or "fx", text = txt or ""
                })
            end
        end
    end
    lf:close()
    os.remove(LINES_FILE)
    
    if #new_lines == 0 then return end
    
    for i = 1, #subs do
        local line = subs[i]
        if line.class == "dialogue" and line.style == style and line.effect ~= "fx" then
            line.comment = true
            subs[i] = line
        end
    end
    
    local pos = #subs + 1
    for _, nl in ipairs(new_lines) do
        subs.insert(pos, nl)
        pos = pos + 1
    end
    
    aegisub.set_undo_point("Py Effector FX")
end

aegisub.register_macro(script_name, script_description, run_effector)
