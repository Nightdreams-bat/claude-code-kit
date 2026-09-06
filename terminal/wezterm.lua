-- wezterm.lua  - base terminal for agentic work on Windows.
-- WezTerm is cross-platform (this same file works on the laptop and on a Mac).
-- It is the Windows stand-in for Ghostty + herder, which are macOS/Linux only.
--
-- Install:  winget install wez.wezterm
-- Then copy this file to  ~\.wezterm.lua

local wezterm = require 'wezterm'
local act = wezterm.action
local config = wezterm.config_builder()

-- ---- look ----
config.color_scheme = 'Catppuccin Mocha'
config.font = wezterm.font_with_fallback { 'Cascadia Code', 'Consolas' }
config.font_size = 11.0
config.window_background_opacity = 0.97
config.enable_scroll_bar = true
config.scrollback_lines = 20000
config.window_decorations = 'RESIZE'
config.default_prog = { 'pwsh.exe', '-NoLogo' }
config.default_cwd = '~/'

-- ---- tab bar: show which pane is which agent ----
config.use_fancy_tab_bar = true
config.tab_max_width = 32
wezterm.on('format-tab-title', function(tab)
  return { { Text = ' ' .. (tab.tab_index + 1) .. ': ' .. tab.active_pane.title .. ' ' } }
end)

-- ---- keys: fast pane/tab management for juggling several agent sessions ----
config.leader = { key = 'a', mods = 'CTRL', timeout_milliseconds = 1000 }
config.keys = {
  { key = '\\', mods = 'LEADER', action = act.SplitHorizontal { domain = 'CurrentPaneDomain' } },
  { key = '-',  mods = 'LEADER', action = act.SplitVertical { domain = 'CurrentPaneDomain' } },
  { key = 'h', mods = 'LEADER', action = act.ActivatePaneDirection 'Left' },
  { key = 'l', mods = 'LEADER', action = act.ActivatePaneDirection 'Right' },
  { key = 'k', mods = 'LEADER', action = act.ActivatePaneDirection 'Up' },
  { key = 'j', mods = 'LEADER', action = act.ActivatePaneDirection 'Down' },
  { key = 'z', mods = 'LEADER', action = act.TogglePaneZoomState },
  { key = 'c', mods = 'LEADER', action = act.SpawnTab 'CurrentPaneDomain' },
  { key = 'x', mods = 'LEADER', action = act.CloseCurrentPane { confirm = true } },
  { key = ',', mods = 'LEADER', action = act.PromptInputLine {
      description = 'tab name:',
      action = wezterm.action_callback(function(win, _, line)
        if line then win:active_tab():set_title(line) end
      end),
  }},
  { key = '1', mods = 'LEADER', action = act.ActivateTab(0) },
  { key = '2', mods = 'LEADER', action = act.ActivateTab(1) },
  { key = '3', mods = 'LEADER', action = act.ActivateTab(2) },
  { key = '4', mods = 'LEADER', action = act.ActivateTab(3) },
  { key = '5', mods = 'LEADER', action = act.ActivateTab(4) },
  { key = '6', mods = 'LEADER', action = act.ActivateTab(5) },
  -- new tab starting a claude session (uses the `cc` alias from your pwsh profile)
  { key = 'n', mods = 'LEADER', action = act.SpawnCommandInNewTab {
      cwd = '~/', args = { 'pwsh.exe', '-NoExit', '-Command', 'cc' },
  }},
}

return config
