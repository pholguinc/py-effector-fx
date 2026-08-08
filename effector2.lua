--[[
	Copyright (c) 2026, Víctor Manuel Payares - All rights reserved.
	
	Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following
	conditions are met:
	
		* Redistributions of source code must retain the above copyright notice, this list of conditions and the following
		  disclaimer.
		* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
		  disclaimer in the documentation and/or other materials provided with the distribution.
		* Neither the name of the EFFECTOR, your author, or the names of its contributors may be used to endorse or promote
		  products derived from this software without specific prior written permission.
	
	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
	INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
	DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
	SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
	LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
	CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
	EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--]]

--[[
	Este es un proyecto apasionado, creado por fans y para fans, diseñado para revolucionar la forma en la que creas y editas
	subtítulos de karaoke y traducciones para videos. Effector no es solo un conjunto de archivos, es una poderosa biblioteca
	de scripts .LUA que te permiten integrar de forma sencilla efectos de karaoke prediseñados de muy alta calidad, funciones
	avanzadas de edición para maximizar tu creatividad en el diseño de efectos, herramientas especializadas para el manejo de
	líneas de traducción y muchas más opciones para llevar tus proyectos gráficos al siguiente nivel. Effector cuenta con una
	amplia y robusta librería que te ofrece un sinfín de posibilidades.
	Podrás ejecutar el listado de efectos que trae por defecto, aunque su verdadero potencial reside en la capacidad de crear
	nuevas librerías personalizadas, diseñar múltiples combinaciones entre todos los efectos y funciones. En su gran mayoría,
	las funciones internas del Effector están diseñadas para emular o ejecutar casi cualquier tipo de efecto gráfico o visual
	que puedas imaginar. Además, incluí una colección de polígonos y figuras ASSdraw (shapes), para los efectos que requieren
	diseño vectorial. El uso de Effector es completamente libre y gratuito. Quiero que este proyecto te pueda servir de punto
	de partida, de plataforma de lanzamiento para que, a partir de ella, puedas crear libremente tus propios efectos, estilos
	y combinaciones. Si deseas apoyarnos, eres libre de incluir el nombre de Effector, los créditos del autor y colaboradores
	en tus proyectos, aunque no es obligatorio.
	Si tienes alguna duda, sugerencia, aporte o, por qué no, deseas formar parte del equipo de desarrollo, contacta conmigo a
	través de https://www.facebook.com/itachi.2021 Si bien animamos a la experimentación, recomendamos encarecidamente evitar
	la modificación del código interno de las funciones y librerías de Effector, a menos que poseas un conocimiento avanzado.
	La alteración sin precaución podría provocar un mal funcionamiento o la inutilización del software. ¡Deseo de corazón que
	Effector te sea de gran utilidad y que disfrutes al máximo creando con él!
--]]
	
	local script_name = "effector2"
	local script_author = "vict8r"
	script_description = "New Generation Effects Automation Subs. Creating Effects with Modifiable Parameters"
	local script_version = "1.0.0"
	local script_update = "august 7th 2026"
	
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
			local fxset = ke.table.copy(sets[fx__.fx_type])
			heads.env.set({fxkara = fxset})
			data.l, data.fxkara, data.fx__ = linei, fxset, fx__
			ke.infofx.styles(data.l, fx__)
			if not fx__.fx_modify then
				for _, fx in ipairs(fxset) do
					if fx.text ~= (fx__.fx_noblank and "" or "ke2") then
						local char, syl, word, line, keep = heads.setcswl(sets, fx, linei, orgline, index)
						local j, maxj, svar, vars = 1, heads.setvarloop(char, syl, word, line, fx)
						data.sets = {["char"] = char, ["syl"] = syl, ["word"] = word, ["line"] = line}
						fx.maxj = maxj
						data.fx = fx
						local var = heads.setvariable(char, syl, word, line, svar, vars, j)
						while fxgroup and j <= maxj do
							line.start_time, line.end_time = orgline.start_time, orgline.end_time
							l.start_time, l.end_time = orgline.start_time, orgline.end_time
							fx.returnfx = nil
							---------------------------------------------------------------------------------
							data.j, data.maxj = j, maxj
							ke.config.temp.valbox(meta, char, syl, word, line, l, fx, var, j, maxj)
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