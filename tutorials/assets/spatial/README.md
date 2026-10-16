# 高德栅格底图

`gaode_style.json`是MapLibre样式，包含一个高德栅格瓦片源和一个raster图层，保留“高德地图”署名。Lonboard的MaplibreBasemap通过HTTP(S)样式URL读取它；Plotly也可直接使用同一瓦片URL。

示例瓦片接口与高德JS API不同，当前不要求在代码格填写JS API Key。瓦片服务需要联网，地址及服务规则以提供方为准。

高德底图使用GCJ-02。04、06的分析几何暂按WGS84作教学演示，源坐标系仍待核实；显示副本通过xyconvert作近似坐标转换，不回写分析表、不用于距离面积统计、不作为标准WGS84数据导出。
显示副本的CRS留空，避免把GCJ-02误标为EPSG:4326。Lonboard因此会提示无CRS，核对这是地图显示副本，而不是遗漏了分析几何的CRS。

[Plotly自定义瓦片](https://plotly.com/python/tile-map-layers/)
[Lonboard底图](https://developmentseed.org/lonboard/latest/api/basemap/)
[MapLibre栅格源](https://maplibre.org/maplibre-style-spec/sources/#raster)
[xyconvert](https://github.com/cyang-kth/xyconvert)
