# 高德栅格底图

`gaode_style.json`是MapLibre样式，包含一个高德栅格瓦片源和一个raster图层，保留“高德地图”署名。Lonboard的MaplibreBasemap通过HTTP(S)样式URL读取它；Plotly也可直接使用同一瓦片URL。

示例瓦片接口与高德JS API不同，当前不要求在代码格填写JS API Key。瓦片服务需要联网，地址及服务规则以提供方为准。

数据提供者已确认微博源坐标为GCJ-02。04—06的原始网格和DataV行政边界直接叠加高德底图，不再调用wgs2gcj，也不把原始几何误标为EPSG:4326。

距离、面积和KDE使用独立分析副本：先以xyconvert.gcj2wgs近似转换数值，再声明EPSG:4326，随后投影到成都附近的EPSG:32648。原始GCJ-02与Parquet保持不变；近似转换不能恢复被网格化的精确位置。

GCJ-02原始/显示几何的CRS留空，因此Lonboard可能提示无CRS；这与已明确声明来源的GCJ-02显示相符。行政边界缓存在`data/spatial/boundaries/`，与底图样式文件分别管理。

[Plotly自定义瓦片](https://plotly.com/python/tile-map-layers/)
[Lonboard底图](https://developmentseed.org/lonboard/latest/api/basemap/)
[MapLibre栅格源](https://maplibre.org/maplibre-style-spec/sources/#raster)
[xyconvert](https://github.com/cyang-kth/xyconvert)
