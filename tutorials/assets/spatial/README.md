# 高德栅格底图

06使用Lonboard的`BitmapTileLayer`直接读取高德栅格瓦片，把瓦片放在数据图层下方；Plotly也使用同一高德瓦片地址。地图加载不依赖课程GitHub Pages提供的样式文件，保留“高德地图”署名。

`gaode_style.json`展示同一瓦片地址的MapLibre配置格式，包含一个栅格源和一个raster图层；当前06和底图测试Notebook不读取此文件。

示例瓦片接口与高德JS API不同，当前不要求在代码格填写JS API Key。瓦片服务需要联网，地址及服务规则以提供方为准。

数据提供者已确认微博源坐标为GCJ-02。04—06的原始网格和DataV行政边界直接叠加高德底图，不再调用wgs2gcj，也不把原始几何误标为EPSG:4326。

距离、面积和KDE使用独立分析副本：先以xyconvert.gcj2wgs近似转换数值，再声明EPSG:4326，随后投影到成都附近的EPSG:32648。原始GCJ-02与Parquet保持不变；近似转换不能恢复被网格化的精确位置。

GCJ-02原始/显示几何的CRS留空，因此Lonboard可能提示无CRS；这与已明确声明来源的GCJ-02显示相符。行政边界缓存在`data/spatial/boundaries/`，与底图样式文件分别管理。

[Plotly自定义瓦片](https://plotly.com/python/tile-map-layers/)
[Lonboard栅格瓦片图层](https://developmentseed.org/lonboard/latest/api/layers/bitmap-tile-layer/)
[MapLibre栅格源](https://maplibre.org/maplibre-style-spec/sources/#raster)
[xyconvert](https://github.com/cyang-kth/xyconvert)
