	script_name		   = "effector2"
	script_description = "New Generation Effects Automation Subs. Creating Effects with Modifiable Parameters"
	script_author	   = "vict8r"
	script_version	   = "1.0 beta"
	script_update	   = "september 29th 2025"
	
	include("karaskel.lua")
	local ke = require("kelibs/newkara_library")
	local ROUND_NUM = 3
	
	ke.config.runfx = function(subs, meta, orgline, sett, fx__, linefx, linei)
		if fx__.fx_printfx then
			ke.config.savefx(fx__)
		else
			ke.infofx.xres, ke.infofx.yres = aegisub.video_size()
			ke.infofx.ratio = ke.math.round((ke.infofx.xres or 1280) / 1280, ROUND_NUM)
			local msa, msb = aegisub.ms_from_frame(1), aegisub.ms_from_frame(101)
			ke.infofx.frame_dur = msb and ke.math.round((msb - msa) / 100, ROUND_NUM) or 41.708
			local l = ke.table.copy(orgline)
			local sets = {
				["char"] = ke.config.text2char(l.text, l.duration, l.styleref, linei.left, linei.top),
				["syl"]  = ke.config.text2syl(l.text, l.duration, l.styleref, linei.left, linei.top),
				["word"] = ke.config.text2word(l.text, l.duration, l.styleref, linei.left, linei.top),
				["line"] = {linei},
			}
			local arrayfx = sets[fx__.fx_type]
			ke.infofx.l = linei
			for _, fx in ipairs(arrayfx) do
				ke.infofx.fx = fx
				local char = sets.char[fx.ci]
				local syl  = sets.syl[fx.si]
				local word = sets.word[fx.wi]
				local line = ke.table.copy(orgline)
				char.n, syl.n, word.n, line.n = #sets.char, #sets.syl, #sets.word, #linefx
				--variables:
				local svar = ("return function(fx__, line, word, syl, ke) %s end"):format(fx__.fx_variable)
				if pcall(loadstring(svar)) then
					loadstring(svar)()(fx__, line, word, syl, ke)
				end
				local var = ke.string.loadstr(fx__.fx_variable, {var = var, syl = syl})
				--loop:
				local loop = {1}
				local sloop = ("return function(fx__, line, word, syl, ke) return {%s} end"):format(fx__.fx_loop)
				if pcall(loadstring(sloop)) then
					loop = loadstring(sloop)()(fx__, line, word, syl, ke)
				end
				ke.infofx.loop = loop
				local j, maxj = 1, 1
				for k, v in pairs(loop)do
					maxj = maxj * v
				end
				while j <= maxj do
					----------------------------------------------------------------
					ke.infofx.j = j
					ke.infofx.maxj = maxj
					ke.config.valbox(fx__, meta, line, l, word, syl, fx, var, ke, j, maxj)
					----------------------------------------------------------------
					l.start_time = fx.time_ini
					l.end_time = fx.time_fin
					l.duration = fx.time_dur
					l.text = ("{%s%s%s}%s"):format(fx.align, fx.pos, fx.add_tags, fx.returnfx)
					l.layer = fx.layer
					subs.append(l)
					j = j + 1
				end
			end
		end
	end
	
	aegisub.register_macro(script_name .. " " .. script_version, script_description, ke.config.macro)
