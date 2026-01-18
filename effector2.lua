	script_name		   = "effector2"
	script_description = "New Generation Effects Automation Subs. Creating Effects with Modifiable Parameters"
	script_author	   = "vict8r"
	script_version	   = "1.0.1 beta"
	script_update	   = "january 18th 2026"
	
	include("karaskel.lua")
	local ke = require("kelibs/newkara_library")
	
	ke.config.runfx = function(subtitles, meta, styles, index, linefx, sett, fx__)
		local data = ke.infofx.data
		local heads = ke.infofx.sethead()
		local fxcount, time_iii = 0, tonumber(os.time())
		for li, xline in ipairs(index) do
			local orgline, linei = subtitles[xline], linefx[li]
			karaskel.preproc_line(subtitles, meta, styles, orgline)
			local l = ke.table.copy(orgline)
			local sets = heads.setlibs(linei)
			local fxset = sets[fx__.fx_type]
			heads.env.set({fxkara = fxset})
			data.l = linei
			if not fx__.fx_modify then
				for _, fx in ipairs(fxset) do
					if fx.text ~= (fx__.fx_noblank and "" or "ke2") then
						local char, syl, word, line, keep = heads.setcswl(sets, fx, linei, orgline, index)
						local j, maxj, svar, vars = 1, heads.setvarloop(char, syl, word, line, fx)
						fx.maxj = maxj
						data.fx = fx
						while fxgroup and j <= maxj do
							local var = heads.setvariable(char, syl, word, line, svar, vars, j)
							---------------------------------------------------------------------------------
							data.j, data.maxj = j, maxj
							ke.config.valbox(meta, char, syl, word, line, l, fx, var, j, maxj)
							fx.add_tags = data.mod_addtags and data.mod_addtags or fx.add_tags
							fx.add_tags = fx__.fx_keept ~= "" and keep .. fx.add_tags or fx.add_tags
							---------------------------------------------------------------------------------
							l.start_time, l.end_time, l.duration = fx.time_ini, fx.time_fin, fx.time_dur
							l.text = ("{%s%s%s}%s"):format(fx.align, fx.pos, fx.add_tags, fx.returnfx)
							l.layer, l.comment = fx.layer, false
							subtitles.insert(#subtitles + 1, l)
							---------------------------------------------------------------------------------
							--local tm = tonumber(os.time()) - time_iii
							--tm = ("%s:%02d:%02d"):format(math.floor(tm / 3600), math.floor(tm / 60) % 60, tm % 60)
							--aegisub.progress.set(100 * fxcount / (#index * fx.n * maxj))
							--aegisub.progress.task(("Lines: [%d/%d]  time: [%s]  Lines Generated: %d"):format(li, #index, tm, fxcount + 1))
							---------------------------------------------------------------------------------
							j = j + 1
							maxj = fx.maxj
							fxcount = fxcount + 1
						end
					end
				end
				orgline.comment = true
			else
				orgline.text = ke.config.modifyline(fx__, meta, orgline, ke)
			end
			subtitles[xline] = orgline
		end
		heads.env.clear()
		ke.recall.reset()
	end
	
	aegisub.register_macro(script_name .. " " .. script_version, script_description, ke.config.macro)