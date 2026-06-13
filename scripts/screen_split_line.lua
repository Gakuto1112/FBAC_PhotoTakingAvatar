---@class (exact) ScreenSplitLines （撮影のための）画面の分割線を管理するクラス
---@field private X_COUNT integer X軸の画面分割数
---@field private Y_COUNT integer Y軸の画面分割数
ScreenSplitLines = {}

---コンストラクタ
---@return ScreenSplitLines
function ScreenSplitLines.new()
	---@type ScreenSplitLines
	local self = instantiate(ScreenSplitLines, nil)

	self.X_COUNT = 3
	self.Y_COUNT = 3

	return self
end

---初期化関数
function ScreenSplitLines:init()
	local parent = models:newPart("script_screen_split_lines", "GUI")
	local screenWidth = client:getScaledWindowSize()
	for x = 1, self.X_COUNT - 1 do
		local lineModel = models.models.zone_display.ZoneDisplayBase:copy(client.intUUIDToString(client.generateUUID()))
		lineModel:setPos(screenWidth.x / self.X_COUNT * x * -1, screenWidth.y * -1, 0)
		lineModel:setScale(1, screenWidth.y, 1)
		lineModel:setVisible(true)
		lineModel:setPrimaryRenderType("EMISSIVE_SOLID")
		parent:addChild(lineModel)
	end
	for y = 1, self.Y_COUNT - 1 do
		local lineModel = models.models.zone_display.ZoneDisplayBase:copy(client.intUUIDToString(client.generateUUID()))
		lineModel:setPos(screenWidth.x * -1, screenWidth.y / self.Y_COUNT * y * -1, 0)
		lineModel:setScale(screenWidth.x, 1, 1)
		lineModel:setVisible(true)
		lineModel:setPrimaryRenderType("EMISSIVE_SOLID")
		parent:addChild(lineModel)
	end

	events.TICK:register(function ()
		parent:setVisible(client:isHudEnabled())
	end)
end

return ScreenSplitLines
