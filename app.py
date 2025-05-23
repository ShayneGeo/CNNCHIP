

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


# import streamlit as st
# import geopandas as gpd
# import rasterio
# import numpy as np
# import matplotlib.pyplot as plt
# import os
# import time
# import gc
# from rasterio.plot import plotting_extent

# st.set_page_config(page_title="Image Chip Viewer", layout="wide")
# st.title("🛰️ Image Chip Generator from GitHub Shapefile + TIFF")
# st.markdown(
#     """
#     This `ImageChipDataset` function reads point locations from a shapefile and, for each point, clips out a small multi-band image patch (a “chip”) directly from your geospatial raster layers—no pre-processing or bulk stack creation required. By computing only the handful of pixels you actually need (and normalizing them on the fly), you save both storage and memory, and you can quickly experiment with different chip sizes or subsets of points without re-running a heavy batch job. This dynamic approach is invaluable when tuning deep learning pipelines (e.g., CNNs) or doing rapid quality checks: you instantly see exactly what data goes into your model, you avoid shipping around huge pre-made datasets, and you keep your workflow nimble and responsive as you iterate on feature selection, model architecture, or sample size.
#     """
# )
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


#             # --- Plot individual rasters with points ---
#             st.subheader("🗺️ Raster Layers with Shapefile Points")
#             fig, axs = plt.subplots(1, len(raster_datasets), figsize=(5 * len(raster_datasets), 5))
#             for i, r in enumerate(raster_datasets):
#                 img = r.read(1)
#                 extent = plotting_extent(r)

#                 axs[i].imshow(img, cmap='gray', extent=extent)
#                 gdf.plot(ax=axs[i], color='red', markersize=10)
#                 axs[i].set_title(f"Raster {i+1}: {os.path.basename(rasterfiles[i])}")
#                 axs[i].axis('off')
#             st.pyplot(fig)

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
#                     axs[i].imshow(chip_array[0][..., i], cmap='gray')
#                     axs[i].set_title(f"Channel {i}")
#                     axs[i].axis('off')
#                 st.pyplot(fig)


#                 # # Optionally allow download
#                 # if st.button("Download Chip Array as .npy"):
#                 #     np.save("chips.npy", chip_array)
#                 #     with open("chips.npy", "rb") as f:
#                 #         st.download_button("Download chips.npy", f, file_name="chips.npy")

#             # --- Memory Cleanup ---
#             # --- Memory Cleanup ---
#             try:
#                 for r in raster_datasets:
#                     r.close()
#                 # only delete these if they exist
#                 if 'chip_array' in locals():
#                     del chip_array
#                 if 'chips' in locals():
#                     del chips
#                 if 'gdf' in locals():
#                     del gdf
#                 if 'raster_datasets' in locals():
#                     del raster_datasets
#                 gc.collect()
#             except Exception:
#                 pass


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
st.markdown(
    """
    This `ImageChipDataset` function reads point locations from a shapefile and, for each point, clips out a small multi-band image patch (a “chip”) 
    directly from your geospatial raster layers—no pre-processing or bulk stack creation required. By computing only the handful of pixels you actually
    need (and normalizing them on the fly), you save both storage and memory, and you can quickly experiment with different chip sizes or subsets of points without re-running a heavy batch job. This dynamic approach is invaluable when tuning deep learning pipelines (e.g., CNNs) or doing rapid quality checks: you instantly see exactly what data goes into your model, you avoid shipping around huge pre-made datasets, and you keep your workflow nimble and responsive as you iterate on feature selection, model architecture, or sample size.
    """
)
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

            # def generate_chip_with_metadata(point):
            #     x, y = point.x, point.y
            #     row, col = raster_datasets[0].index(x, y)
            #     h = chip_size // 2
            #     win = rasterio.windows.Window(col - h, row - h, chip_size, chip_size)
                
            #     chip_stack = []
            #     center_values = []
            #     for i, r in enumerate(raster_datasets):
            #         chip = r.read(1, window=win)
            #         chip = np.expand_dims(chip, axis=-1)
            #         chip = (chip - mins[i]) / (maxs[i] - mins[i])
            #         chip_stack.append(chip)
            
            #         center_val = r.read(1, window=rasterio.windows.Window(col, row, 1, 1))[0, 0]
            #         center_val = (center_val - mins[i]) / (maxs[i] - mins[i])
            #         center_values.append(center_val)
            def is_window_within_bounds(window, height, width):
                return (
                    window.col_off >= 0 and
                    window.row_off >= 0 and
                    window.col_off + window.width <= width and
                    window.row_off + window.height <= height
                )

            
            #     return np.concatenate(chip_stack, axis=-1), np.array(center_values)
            def generate_chip_with_metadata(point):
                x, y = point.x, point.y
                row, col = raster_datasets[0].index(x, y)
                h = chip_size // 2
                win = rasterio.windows.Window(col - h, row - h, chip_size, chip_size)
            
                if not is_window_within_bounds(win, raster_datasets[0].height, raster_datasets[0].width):
                    raise ValueError("Point too close to edge of raster")

                
                chip_stack = []
                center_values = []
                for i, r in enumerate(raster_datasets):
                    chip = r.read(1, window=win)
                    chip = np.expand_dims(chip, axis=-1)
                    chip = (chip - mins[i]) / (maxs[i] - mins[i])
                    chip_stack.append(chip)
            
                    center_val = r.read(1, window=rasterio.windows.Window(col, row, 1, 1))[0, 0]
                    center_val = (center_val - mins[i]) / (maxs[i] - mins[i])
                    center_values.append(center_val)
            
                # Add normalized lat/lon to the end of the metadata vector
                #center_values.append((y + 90) / 180)  # normalize latitude [-90,90] → [0,1]
                #center_values.append((x + 180) / 360)  # normalize longitude [-180,180] → [0,1]

                center_values.append(y)  # latitude
                center_values.append(x)  # longitude

                
                return np.concatenate(chip_stack, axis=-1), np.array(center_values)




            chips = []
            metadata = []
            
            start_time = time.time()
            for idx in range(len(gdf)):
                try:
                    chip, meta = generate_chip_with_metadata(gdf.geometry.iloc[idx])
                    chips.append(chip)
                    metadata.append(meta)
                except Exception as e:
                    st.warning(f"Skipping point {idx} due to error: {e}")
            end_time = time.time()
            st.success(f"Generated {len(chips)} chips in {end_time - start_time:.2f} seconds")
            estimated_total_time = (end_time - start_time) * (1_000_000 / len(chips))
            st.info(f"Estimated time for 1,000,000 chips: {estimated_total_time / 60:.2f} minutes (~{estimated_total_time / 3600:.2f} hours)")


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
            chip_array = np.stack(chips)
            metadata_array = np.stack(metadata)
            
            st.write(f"Chip array shape: {chip_array.shape}")
            st.write(f"Metadata array shape: {metadata_array.shape}")
            st.write(f"{metadata_array}")
            


                # # Optionally allow download
                # if st.button("Download Chip Array as .npy"):
                #     np.save("chips.npy", chip_array)
                #     with open("chips.npy", "rb") as f:
                #         st.download_button("Download chips.npy", f, file_name="chips.npy")

            # --- Memory Cleanup ---
            # --- Memory Cleanup ---
            try:
                for r in raster_datasets:
                    r.close()
                # only delete these if they exist
                if 'chip_array' in locals():
                    del chip_array
                if 'chips' in locals():
                    del chips
                if 'gdf' in locals():
                    del gdf
                if 'raster_datasets' in locals():
                    del raster_datasets
                gc.collect()
            except Exception:
                pass


    else:
        st.error("Shapefile or TIFF files not found in expected paths. Make sure 'myfolder/' directory exists in repo.")





