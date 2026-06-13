BASE_POS = vectors.vec3(238.5, 64, 1276.5)

---モデルの親タイプをリセットする。
---指定したモデルのサブモデルも対象となる。
---@param model ModelPart リセット対象のモデルパーツ
function resetModelParent(model)
	model:setParentType("None")
	if model:getType() == "GROUP" then
		if model:getName():match("Halo") then
			model:setLight(15, 15)
		end
		for _, child in ipairs(model:getChildren()) do
			resetModelParent(child)
		end
	end
end

---クラスをインスタンス化する。
---@generic S
---@generic C
---@param class `C` インスタンス化するクラス
---@param super? `S` インスタンス化するクラスのスーパークラス
---@param ... any クラスのインスタンス時に渡される引数
---@return C instance インスタンス化されたクラスのオブジェクト
---@diagnostic disable-next-line: lowercase-global
function instantiate(class, super, ...)
	local instance = super and super.new(...) or {}
	setmetatable(instance, {__index = class})
	setmetatable(class, {__index = super})
	return instance
end

require("scripts.screen_split_line")
local screenSplitLines = ScreenSplitLines.new()
screenSplitLines:init()

models.models.main.World:setPos(BASE_POS:copy():scale(16))
for _, modelPart in ipairs(models.models.main.World:getChildren()) do
	resetModelParent(modelPart)
end
events.TICK:register(function ()
	for _, modelPart in ipairs(models.models.main.World:getChildren()) do
		local pos = BASE_POS:copy():add(modelPart:getPivot():scale(1 / 16):mul(-1, 1, 1))
		modelPart:setLight(world.getBlockLightLevel(pos), world.getSkyLightLevel(pos))
	end
end)
