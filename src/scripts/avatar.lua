---撮影アバターの基準ワールド座標
---@type Vector3
BASE_POS = vectors.vec3(0, 0, 0)

---ワールドに配置したキャラクターのライティング判定基準点のオフセット座標
---キャラクターが暗くなってしまう場合はこのオフセット値のY座標を上げると解決する場合がある。
---@type Vector3
CHARACTER_LIGHTING_BASE_POINT_OFFSET = vectors.vec3(0, 0, 0)

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

---指定したモデルのワールド位置を返す。
---@param model ModelPart ワールド位置を取得するモデルパーツ
---@return Vector3 worldPos モデルのワールド位置
local function getModelWorldPos(model)
	local modelMatrix = model:partToWorldMatrix()
	return vectors.vec3(modelMatrix[4][1], modelMatrix[4][2], modelMatrix[4][3])
end

---初期化時に実行されるコールバック関数
local function onInit()
	-- ここに追加の処理を書く。


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
			local pos = BASE_POS:copy():add(modelPart:getPivot():scale(1 / 16):mul(-1, 1, 1):add(CHARACTER_LIGHTING_BASE_POINT_OFFSET))
			modelPart:setLight(world.getBlockLightLevel(pos), world.getSkyLightLevel(pos))
		end
	end)

	onInit()
end

init()
