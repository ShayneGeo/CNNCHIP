

# import streamlit as st
# import geopandas as gpd
# import rasterio
# import numpy as np
# import matplotlib.pyplot as plt
# import os
# import time
# import gc

# st.set_page_config(page_title="Image Chip Viewer", layout="wide")
# st.title("🛰️ Image Chip Generator from GitHub Shapefile + TIFF")

# # --- Parameters ---
# subset = st.number_input("Number of Points to Process", min_value=1, max_value=10000, value=1000)
# chip_size = st.selectbox("Chip Size (pixels)", [16, 32, 64, 128, 256], index=1)
# run_button = st.button("Run Chip Generation")

# # --- File paths in repo ---
# shapefile = "myfolder/Antelope.shp"
# rasterfiles = [
#     "myfolder/LC20_Asp_220_SMALL.tif",
#     "myfolder/LC20_SlpD_220_SMALL.tif",
#     "myfolder/LC22_EVH_220_SMALL.tif"
# ]

# # --- Load and Process ---
# if run_button:
#     if os.path.exists(shapefile) and all(os.path.exists(f) for f in rasterfiles):
#         with st.spinner("Loading data and generating chips..."):
#             gdf = gpd.read_file(shapefile)
#             if gdf.crs is None or gdf.crs.to_epsg() != 4326:
#                 gdf = gdf.to_crs(epsg=4326)
#             gdf = gdf.iloc[:subset]

#             raster_datasets = [rasterio.open(fp) for fp in rasterfiles]
#             mins, maxs = [], []
#             for r in raster_datasets:
#                 band = r.read(1)
#                 band = np.where(band == -9999, 0, band)
#                 mins.append(band.min())
#                 maxs.append(band.max())

#             def generate_chip(point):
#                 x, y = point.x, point.y
#                 row, col = raster_datasets[0].index(x, y)
#                 h = chip_size // 2
#                 win = rasterio.windows.Window(col-h, row-h, chip_size, chip_size)
#                 chip_stack = []
#                 for i, r in enumerate(raster_datasets):
#                     chip = r.read(1, window=win)
#                     chip = np.expand_dims(chip, axis=-1)
#                     chip = (chip - mins[i]) / (maxs[i] - mins[i])
#                     chip_stack.append(chip)
#                 return np.concatenate(chip_stack, axis=-1)

#             chips = []
#             start_time = time.time()
#             for idx in range(len(gdf)):
#                 try:
#                     chip = generate_chip(gdf.geometry.iloc[idx])
#                     chips.append(chip)
#                 except Exception as e:
#                     st.warning(f"Skipping point {idx} due to error: {e}")

#             end_time = time.time()
#             st.success(f"Generated {len(chips)} chips in {end_time - start_time:.2f} seconds")

#             if chips:
#                 chip_array = np.stack(chips)
#                 st.write(f"Chip array shape: {chip_array.shape}")

#                 # Plot the first chip
#                 st.subheader("Example Chip")
#                 fig, axs = plt.subplots(1, chip_array.shape[-1], figsize=(4 * chip_array.shape[-1], 4))
#                 for i in range(chip_array.shape[-1]):
#                     axs[i].imshow(chip_array[100][..., i], cmap='gray')
#                     axs[i].set_title(f"Channel {i}")
#                     axs[i].axis('off')
#                 st.pyplot(fig)


#                 # Optionally allow download
#                 if st.button("Download Chip Array as .npy"):
#                     np.save("chips.npy", chip_array)
#                     with open("chips.npy", "rb") as f:
#                         st.download_button("Download chips.npy", f, file_name="chips.npy")

#             # --- Memory Cleanup ---
#             for r in raster_datasets:
#                 r.close()
#             del chip_array, chips, gdf, raster_datasets
#             gc.collect()

#     else:
#         st.error("Shapefile or TIFF files not found in expected paths. Make sure 'myfolder/' directory exists in repo.")


import streamlit as st
import geopandas as gpd
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import os
import time
import gc
from rasterio.plot import plotting_extent

st.set_page_config(page_title="Image Chip Viewer", layout="wide")
st.title("🛰️ Image Chip Generator from GitHub Shapefile + TIFF")

# --- Parameters ---
subset = st.number_input("Number of Points to Process", min_value=1, max_value=10000, value=1000)
chip_size = st.selectbox("Chip Size (pixels)", [16, 32, 64, 128, 256], index=1)
run_button = st.button("Run Chip Generation")

# --- File paths in repo ---
shapefile = "myfolder/Antelope.shp"
rasterfiles = [
    "myfolder/LC20_Asp_220_SMALL.tif",
    "myfolder/LC20_SlpD_220_SMALL.tif",
    "myfolder/LC22_EVH_220_SMALL.tif"
]

# --- Load and Process ---
if run_button:
    if os.path.exists(shapefile) and all(os.path.exists(f) for f in rasterfiles):
        with st.spinner("Loading data and generating chips..."):
            gdf = gpd.read_file(shapefile)
            if gdf.crs is None or gdf.crs.to_epsg() != 4326:
                gdf = gdf.to_crs(epsg=4326)
            gdf = gdf.iloc[:subset]

            raster_datasets = [rasterio.open(fp) for fp in rasterfiles]
            mins, maxs = [], []
            for r in raster_datasets:
                band = r.read(1)
                band = np.where(band == -9999, 0, band)
                mins.append(band.min())
                maxs.append(band.max())


            # --- Plot individual rasters with points ---
            st.subheader("🗺️ Raster Layers with Shapefile Points")
            fig, axs = plt.subplots(1, len(raster_datasets), figsize=(5 * len(raster_datasets), 5))
            for i, r in enumerate(raster_datasets):
                img = r.read(1)
                extent = plotting_extent(r)

                axs[i].imshow(img, cmap='gray', extent=extent)
                gdf.plot(ax=axs[i], color='red', markersize=10)
                axs[i].set_title(f"Raster {i+1}: {os.path.basename(rasterfiles[i])}")
                axs[i].axis('off')
            st.pyplot(fig)

            def generate_chip(point):
                x, y = point.x, point.y
                row, col = raster_datasets[0].index(x, y)
                h = chip_size // 2
                win = rasterio.windows.Window(col-h, row-h, chip_size, chip_size)
                chip_stack = []
                for i, r in enumerate(raster_datasets):
                    chip = r.read(1, window=win)
                    chip = np.expand_dims(chip, axis=-1)
                    chip = (chip - mins[i]) / (maxs[i] - mins[i])
                    chip_stack.append(chip)
                return np.concatenate(chip_stack, axis=-1)

            chips = []
            start_time = time.time()
            for idx in range(len(gdf)):
                try:
                    chip = generate_chip(gdf.geometry.iloc[idx])
                    chips.append(chip)
                except Exception as e:
                    st.warning(f"Skipping point {idx} due to error: {e}")

            end_time = time.time()
            st.success(f"Generated {len(chips)} chips in {end_time - start_time:.2f} seconds")

            if chips:
                chip_array = np.stack(chips)
                st.write(f"Chip array shape: {chip_array.shape}")

                # Plot the first chip
                st.subheader("Example Chip")
                fig, axs = plt.subplots(1, chip_array.shape[-1], figsize=(4 * chip_array.shape[-1], 4))
                for i in range(chip_array.shape[-1]):
                    axs[i].imshow(chip_array[0][..., i], cmap='gray')
                    axs[i].set_title(f"Channel {i}")
                    axs[i].axis('off')
                st.pyplot(fig)


                # Optionally allow download
                if st.button("Download Chip Array as .npy"):
                    np.save("chips.npy", chip_array)
                    with open("chips.npy", "rb") as f:
                        st.download_button("Download chips.npy", f, file_name="chips.npy")

            # --- Memory Cleanup ---
            for r in raster_datasets:
                r.close()
            del chip_array, chips, gdf, raster_datasets
            gc.collect()

    else:
        st.error("Shapefile or TIFF files not found in expected paths. Make sure 'myfolder/' directory exists in repo.")







