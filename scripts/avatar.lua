---撮影アバターの基準ワールド座標
BASE_POS = vectors.vec3(0, 0, 0)

---モデルの親タイプをリセットする。
---指定したモデルのサブモデルも対象となる。
---@param model ModelPart リセット対象のモデルパーツ
local function resetModelParent(model)
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

---初期化関数
local function init()
	local screenSplitLines = require("scripts.screen_split_line")
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
end

init()
