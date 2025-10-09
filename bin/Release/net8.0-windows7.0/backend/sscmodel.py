import xml.etree.ElementTree as ET
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
from typing import List
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import traceback

from .adcp import ADCP as ADCPDataset
from .obs import OBS as OBSDataset
from .watersample import WaterSample as WaterSampleDataset
from .utils_xml import XMLUtils
from .plotting import PlottingShell


def NTU2SSC(project: ET.Element, sscmodel: ET.Element) -> dict:
    proj_xml = XMLUtils(project)
    ssc_params = {}
    mode = sscmodel.find("Mode").text
    if mode == "Manual":
        A = float(sscmodel.find("A").text)
        B = float(sscmodel.find("B").text)
        ssc_params['A'] = A
        ssc_params['B'] = B
        return ssc_params
    elif mode == "Auto":
        obss = []
        obsIDs = []
        watersamples = []
        watersampleIDs = []
        for inst in sscmodel.findall("Instrument"):
            inst_id = inst.find("ID").text
            inst_type = inst.find("Type").text
            if inst_type == "OBSVerticalProfile":
                cfg = proj_xml.get_cfg_by_instrument(inst_type, None, inst_id, add_ssc=False)
                obss.append(OBSDataset(cfg))
                obsIDs.append(inst_id)
            elif inst_type == "WaterSample":
                watersamples.append(WaterSampleDataset(proj_xml.find_element(elem_id=inst_id, _type=inst_type)))
                watersampleIDs.append(inst_id)
        if len(watersamples) == 0:
            return {"Error": "No water samples found for SSC calibration"}
        if len(obss) == 0:
            return {"Error": "No OBS data found for SSC calibration"}
        df_obs = combine_obs(obss, obsIDs)
        df_water = combine_watersamples(watersamples, watersampleIDs)

        parameters = calculate_params(from_df=df_water,
                                      from_col_name="ssc",
                                      from_id_name="SSC",
                                      to_df=df_obs,
                                      to_col_name="ntu",
                                      to_id_name="NTU",
                                      time_tolerance=None,
                                      depth_tolerance=1,
                                      fit_intercept=False,
                                      relation="linear",
                                      weighted=True)

        for key, value in parameters.items():
            ssc_params[key] = value
        return ssc_params

def PlotNTU2SSC(project: ET.Element, sscmodelid: str, title: str = None):
    proj_xml = XMLUtils(project)
    sscmodel = proj_xml.find_element(elem_id=sscmodelid, _type='NTU2SSC')
    if sscmodel is None:
        return {"Error": f"No NTU2SSC model found with ID {sscmodelid}"}
    try:
        A = float(sscmodel.find("A").text)
        B = float(sscmodel.find("B").text)
        RMSE = float(sscmodel.find("RMSE").text)
        R2 = float(sscmodel.find("R2").text)

        # Extract data points
        ssc = []
        ntu = []
        for pt in sscmodel.find("Data").findall("Point"):
            ssc.append(float(pt.find("SSC").text))
            ntu.append(float(pt.find("NTU").text))
        ssc = np.array(ssc)
        ntu = np.array(ntu)

        fig, ax = PlottingShell.subplots(figheight=8, figwidth=8)
        ax.scatter(ssc, ntu, label="Data Points", color=PlottingShell.red2)
        x = np.linspace(min(ssc), max(ssc), 100)
        y = (x - A) / B
        ax.plot(x, y, label='Fitted Regression', color=PlottingShell.blue3)
        ax.legend()
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('SSC')
        ax.set_ylabel('NTU')
        equation = r"$\mathrm{SSC} = A + B \times \mathrm{NTU}$"
        textstr = f"{equation}\nA = {A:.3f}\nB = {B:.3f}\nRMSE = {RMSE:.2f}\nR² = {R2:.3f}"
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes,
                fontsize=10, verticalalignment="top",
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.7))
        ax.grid(True, alpha=0.5)
        if title is not None:
            ax.set_title(title)
        plt.show()
        return {"Result": "Success"}
    except Exception as e:
        return {"Error": str(e)}

def BKS2SSC(project: ET.Element, sscmodel: ET.Element) -> dict:
    proj_xml = XMLUtils(project)
    ssc_params = {}
    mode = sscmodel.find("Mode").text
    if mode == "Manual":
        A = float(sscmodel.find("A").text)
        B = float(sscmodel.find("B").text)
        ssc_params['A'] = A
        ssc_params['B'] = B
        return ssc_params
    elif mode == "Auto":
        adcps = []
        adcpIDs = []
        watersamples = []
        watersampleIDs = []
        for inst in sscmodel.findall("Instrument"):
            inst_id = inst.find("ID").text
            inst_type = inst.find("Type").text
            if inst_type == "VesselMountedADCP":
                cfg = proj_xml.get_cfg_by_instrument("VesselMountedADCP", instrument_id=inst_id, add_ssc=False)
                adcps.append(ADCPDataset(cfg, name=cfg['name']))
                adcpIDs.append(inst_id)
            elif inst_type == "WaterSample":
                watersamples.append(WaterSampleDataset(proj_xml.find_element(elem_id=inst_id, _type=inst_type)))
                watersampleIDs.append(inst_id)
        if len(watersamples) == 0:
            return {"Error": "No water samples found for SSC calibration"}
        if len(adcps) == 0:
            return {"Error": "No ADCP data found for SSC calibration"}
        df_adcp = combine_adcps(adcps, adcpIDs)
        df_adcp["depth"] = -df_adcp["depth"]  # Convert to positive down
        df_adcp = df_adcp.sort_values("datetime")
        df_water = combine_watersamples(watersamples, watersampleIDs)

        parameters = calculate_params(from_df=df_water,
                                      from_col_name="ssc",
                                      from_id_name="SSC",
                                      to_df=df_adcp,
                                      to_col_name="bks",
                                      to_id_name="AbsoluteBackscatter",
                                      time_tolerance="2min",
                                      depth_tolerance=2,
                                      fit_intercept=True,
                                      relation="loglinear",
                                      weighted=True)

        for key, value in parameters.items():
            ssc_params[key] = value
        return ssc_params

def PlotBKS2SSC(project: ET.Element, sscmodelid: str, title: str) -> dict:
    proj_xml = XMLUtils(project)
    sscmodel = proj_xml.find_element(elem_id=sscmodelid, _type='BKS2SSC')
    if sscmodel is None:
        return {"Error": f"No BKS2SSC model found with ID {sscmodelid}"}
    try:
        A = float(sscmodel.find("A").text)
        B = float(sscmodel.find("B").text)
        RMSE = float(sscmodel.find("RMSE").text)
        R2 = float(sscmodel.find("R2").text)

        # Extract data points
        ssc = []
        bks = []
        for pt in sscmodel.find("Data").findall("Point"):
            ssc.append(float(pt.find("SSC").text))
            bks.append(float(pt.find("AbsoluteBackscatter").text))
        ssc = 10 ** (np.array(ssc))
        bks = np.array(bks)

        fig, ax = PlottingShell.subplots(figheight=8, figwidth=8)
        ax.scatter(ssc, bks, label="Data Points", color=PlottingShell.red2)
        x = np.linspace(0.9*min(ssc), 1.1*max(ssc), 100)
        y = (np.log10(x) - A) / B
        ax.plot(x, y, label='Fitted Regression', color=PlottingShell.blue3)
        ax.set_xscale('log')
        ax.set_xlim(min(ssc)*0.9, max(ssc)*1.1)
        ax.set_ylim(np.floor(min(bks)*1.1), np.ceil(max(bks)*0.9))
        ax.legend()
        ax.set_xlabel('SSC')
        ax.set_ylabel('Absolute Backscatter')
        equation = r"$\log_{10}(\mathrm{SSC}) = A + B \times \mathrm{BKS}$"
        textstr = f"{equation}\nA = {A:.3f}\nB = {B:.3f}\nRMSE = {RMSE:.2f}\nR² = {R2:.3f}"
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes,
                fontsize=10, verticalalignment="top",
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.7))
        ax.grid(True, alpha=0.5)
        if title is not None:
            ax.set_title(title)
        plt.show()
        return {"Result": "Success"}
    except Exception as e:
        return {"Error": str(e)}

def PlotBKS2SSCTrans(project, sscmodelid, beam_sel, field_name, yAxisMode, cmap, vmin, vmax, title, mask):
    field_name_map = {
        "Velocity": "velocity",
        "Echo Intensity": "echo_intensity",
        "Correlation Magnitude": "correlation_magnitude",
        "Percent Good": "percent_good",
        "Absolute Backscatter": "absolute_backscatter",
        "Alpha S": "alpha_s",
        "Alpha W": "alpha_w",
        "Signal to Noise Ratio": "signal_to_noise_ratio",
        "SSC": "suspended_solids_concentration",
    }
    try:
        proj_xml = XMLUtils(project)
        sscmodel = proj_xml.find_element(elem_id=sscmodelid, _type='BKS2SSC')
        if sscmodel is None:
            return {"Error": f"No BKS2SSC model found with ID {sscmodelid}"}
        pairs = sscmodel.find("Pairs").findall("Pair")
        for pair in pairs:
            water_sample_id = pair.find("WaterSample").text
            adcp_id = pair.find("VesselMountedADCP").text
            if water_sample_id is None or adcp_id is None:
                return {"Error": "No valid WaterSample-ADCP pairs found in the SSC model"}
            adcp_cfg = proj_xml.get_cfg_by_instrument("VesselMountedADCP", instrument_id=adcp_id, add_ssc=True)
            if 'Error' in adcp_cfg.keys():
                return adcp_cfg
            water_sample_cfg = proj_xml.find_element(elem_id=water_sample_id, _type="WaterSample")
            if water_sample_cfg is None:
                return {"Error": f"No WaterSample found with ID {water_sample_id}"}
            adcp = ADCPDataset(adcp_cfg, name = adcp_cfg['name'])
            water_sample = WaterSampleDataset(water_sample_cfg)

            fig, (ax, ax_cbar) = adcp.plot.single_beam_flood_plot(
                beam = beam_sel,
                field_name = field_name_map[field_name],
                y_axis_mode = yAxisMode.lower(),
                cmap = cmap,
                vmin = vmin,
                vmax = vmax,
                n_time_ticks = 6,
                title = title, 
                mask = mask
                )
            t_num = mdates.date2num(water_sample.data.datetime.astype("M8[ms]").astype("O"))
            x_min, x_max = ax.get_xlim()
            y_min, y_max = ax.get_ylim()
            mask = (t_num >= x_min) & (t_num <= x_max) & (water_sample.data.depth >= min(y_min, y_max)) & (water_sample.data.depth <= max(y_min, y_max))

            # Filter data
            t_num = t_num[mask]
            depth = water_sample.data.depth[mask]
            sample = water_sample.data.sample[mask]
            ax.scatter(t_num, depth, marker="*", zorder=100, label="Water Samples", s=20)
            for t, d, s in zip(t_num, depth, sample):
                ax.text(t, d, s, va="bottom", ha="center", fontsize=7,
                        bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.7))
            fig.canvas.draw()
            ax.legend(loc="lower right", fontsize=8)
            plt.show()
        return {"Result": str(adcp._cfg)}
    except Exception as e:
        tb_str = traceback.format_exc()
        return {"Error": tb_str + "\n" + str(e)}

def BKS2NTU(project: ET.Element, sscmodel: ET.Element) -> dict:
    proj_xml = XMLUtils(project)
    ssc_params = {}
    mode = sscmodel.find("Mode").text
    if mode == "Manual":
        A = float(sscmodel.find("A").text)
        B = float(sscmodel.find("B").text)
        ssc_params['A'] = A
        ssc_params['B'] = B
        return ssc_params
    elif mode == "Auto":
        adcps = []
        adcpIDs = []
        obss = []
        obsIDs = []
        for inst in sscmodel.findall("Instrument"):
            inst_id = inst.find("ID").text
            inst_type = inst.find("Type").text
            if inst_type == "VesselMountedADCP":
                cfg = proj_xml.get_cfg_by_instrument(inst_type, instrument_id=inst_id, add_ssc=False)
                adcps.append(ADCPDataset(cfg, name=cfg['name']))
                adcpIDs.append(inst_id)
            elif inst_type == "OBSVerticalProfile":
                cfg = proj_xml.get_cfg_by_instrument(inst_type, None, inst_id, add_ssc=True)
                obss.append(OBSDataset(cfg))
                obsIDs.append(inst_id)
        if len(obss) == 0:
            return {"Error": "No OBSVerticalProfile found for SSC calibration"}
        if len(adcps) == 0:
            return {"Error": "No ADCP data found for SSC calibration"}
        df_adcp = combine_adcps(adcps, adcpIDs)
        df_adcp["depth"] = -df_adcp["depth"]  # Convert to positive down
        df_adcp = df_adcp.sort_values("datetime")
        df_obs = combine_obs(obss, obsIDs, by_ssc=True)

        parameters = calculate_params(from_df=df_obs,
                                      from_col_name="ntu",
                                      from_id_name="SSC",
                                      to_df=df_adcp,
                                      to_col_name="bks",
                                      to_id_name="AbsoluteBackscatter",
                                      time_tolerance="10s",
                                      depth_tolerance=0.5,
                                      fit_intercept=True,
                                      relation="loglinear",
                                      weighted=True)
        
        for key, value in parameters.items():
            ssc_params[key] = value
        return ssc_params

def PlotBKS2NTU(project: ET.Element, sscmodelid: str, title: str) -> dict:
    proj_xml = XMLUtils(project)
    sscmodel = proj_xml.find_element(elem_id=sscmodelid, _type='BKS2NTU')
    if sscmodel is None:
        return {"Error": f"No BKS2NTU model found with ID {sscmodelid}"}
    try:
        A = float(sscmodel.find("A").text)
        B = float(sscmodel.find("B").text)
        RMSE = float(sscmodel.find("RMSE").text)
        R2 = float(sscmodel.find("R2").text)

        # Extract data points
        ntu = []
        bks = []
        for pt in sscmodel.find("Data").findall("Point"):
            ntu.append(float(pt.find("SSC").text))
            bks.append(float(pt.find("AbsoluteBackscatter").text))
        ntu = 10 ** (np.array(ntu))
        bks = np.array(bks)

        fig, ax = PlottingShell.subplots(figheight=8, figwidth=8)
        ax.scatter(ntu, bks, label="Data Points", color=PlottingShell.red2)
        x = np.linspace(0.9*min(ntu), 1.1*max(ntu), 100)
        y = (np.log10(x) - A) / B
        ax.plot(x, y, label='Fitted Regression', color=PlottingShell.blue3)
        ax.set_xscale('log')
        ax.set_xlim(min(ntu)*0.9, max(ntu)*1.1)
        ax.set_ylim(np.floor(min(bks)*1.1), np.ceil(max(bks)*0.9))
        ax.legend()
        ax.set_xlabel('SSC')
        ax.set_ylabel('Absolute Backscatter')
        equation = r"$\log_{10}(\mathrm{SSC}) = A + B \times \mathrm{BKS}$"
        textstr = f"{equation}\nA = {A:.3f}\nB = {B:.3f}\nRMSE = {RMSE:.2f}\nR² = {R2:.3f}"
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes,
                fontsize=10, verticalalignment="top",
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.7))
        ax.grid(True, alpha=0.5)
        if title is not None:
            ax.set_title(title)
        plt.show()
        return {"Result": "Success"}
    except Exception as e:
        return {"Error": str(e)}

def PlotBKS2NTUTrans(project, sscmodelid, beam_sel, field_name, yAxisMode, cmap, vmin, vmax, title, mask):
    field_name_map = {
        "Velocity": "velocity",
        "Echo Intensity": "echo_intensity",
        "Correlation Magnitude": "correlation_magnitude",
        "Percent Good": "percent_good",
        "Absolute Backscatter": "absolute_backscatter",
        "Alpha S": "alpha_s",
        "Alpha W": "alpha_w",
        "Signal to Noise Ratio": "signal_to_noise_ratio",
        "SSC": "suspended_solids_concentration",
    }
    try:
        proj_xml = XMLUtils(project)
        sscmodel = proj_xml.find_element(elem_id=sscmodelid, _type='BKS2NTU')
        if sscmodel is None:
            return {"Error": f"No BKS2NTU model found with ID {sscmodelid}"}
        pairs = sscmodel.find("Pairs").findall("Pair")
        for pair in pairs:
            obs_id = pair.find("OBSVerticalProfile").text
            adcp_id = pair.find("VesselMountedADCP").text
            if obs_id is None or adcp_id is None:
                return {"Error": "No valid OBS-ADCP pairs found in the SSC model"}
            adcp_cfg = proj_xml.get_cfg_by_instrument("VesselMountedADCP", instrument_id=adcp_id, add_ssc=True)
            if 'Error' in adcp_cfg.keys():
                return adcp_cfg
            obs_cfg = proj_xml.get_cfg_by_instrument("OBSVerticalProfile", instrument_id=obs_id, add_ssc=True)
            if 'Error' in obs_cfg.keys():
                return obs_cfg
            adcp = ADCPDataset(adcp_cfg, name = adcp_cfg['name'])
            obs = OBSDataset(obs_cfg)
            fig, (ax, ax_cbar) = adcp.plot.single_beam_flood_plot(
                beam = beam_sel,
                field_name = field_name_map[field_name],
                y_axis_mode = yAxisMode.lower(),
                cmap = cmap,
                vmin = vmin,
                vmax = vmax,
                n_time_ticks = 6,
                title = title, 
                mask = mask
                )
            t_num = mdates.date2num(obs.data.datetime.astype("M8[ms]").astype("O"))
            x_min, x_max = ax.get_xlim()
            y_min, y_max = ax.get_ylim()
            data_mask = (t_num >= x_min) & (t_num <= x_max) & (obs.data.depth >= min(y_min, y_max)) & (obs.data.depth <= max(y_min, y_max))
            
            im = ax.images[0]
            norm = im.norm
            cmap = im.cmap

            # Filter data
            t_num = t_num[data_mask]
            depth = obs.data.depth[data_mask]
            ssc = obs.data.ssc[data_mask]
            ax.scatter(t_num, depth, marker="*", zorder=100, label=obs.name, s=20)
            fig.canvas.draw()
            ax.legend(loc="lower right", fontsize=8)
            plt.show()
        return {"Result": str(adcp._cfg)}
    except Exception as e:
        tb_str = traceback.format_exc()
        return {"Error": tb_str + "\n" + str(e)}

# -- Helper functions for sscmodel.py --

def combine_adcps(adcp_list: List[ADCPDataset], adcp_ids: List[str]):
    dfs = []
    for i, adcp in enumerate(adcp_list):
        datetimes = adcp.time.ensemble_datetimes
        abs_bks = adcp.get_beam_data(field_name="absolute_backscatter", mask=True)
        depths = adcp.geometry.geographic_beam_midpoint_positions.z
        abs_bks = np.nanmean(abs_bks, axis=2)  # average across beams (n_ensembels, n_bins, n_beams) -> (n_ensembles * n_bins * n_beams)
        depths = np.nanmean(depths, axis=2)  # average across beams
        datetimes = np.repeat(datetimes[:, None], abs_bks.shape[1], axis=1)
        df = pd.DataFrame({
            "datetime": datetimes.ravel(),
            "depth": depths.ravel(),
            "bks": abs_bks.ravel(),
            "id": adcp_ids[i],
            "type": "VesselMountedADCP"
        })
        dfs.append(df)
    output = pd.concat(dfs, ignore_index=True)
    output = output.dropna(subset=["bks"])
    return output

def combine_obs(obs_list: List[OBSDataset], obs_ids: List[str], by_ssc: bool = False):
    dfs = []
    for i, obs in enumerate(obs_list):
        if by_ssc:
            data = obs.data.ssc
        else:
            data = obs.data.ntu
        df = pd.DataFrame({
            "datetime": obs.data.datetime,
            "depth": obs.data.depth,
            "ntu": data,
            "id": obs_ids[i],
            "type": "OBSVerticalProfile"
        })
        dfs.append(df)
    output = pd.concat(dfs, ignore_index=True)
    output = output.dropna(subset=["ntu"])
    return output

def combine_watersamples(water_list: List[WaterSampleDataset], water_ids: List[str]):
    dfs = []
    for i, water in enumerate(water_list):
        df = pd.DataFrame({
            "datetime": water.data.datetime,
            "depth": water.data.depth,
            "ssc": water.data.ssc,
            "id": water_ids[i],
            "type": "WaterSample"
        })
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

def match_datasets(
    x_df, y_df,
    x_col_name, y_col_name,
    time_tolerance=None, depth_tolerance=None
):
    """
    For each row in source, find the closest row in target.
    Priority:
      1. Minimize depth difference
      2. If tie, minimize datetime difference

    Parameters
    ----------
    source : DataFrame
        The dataframe driving the matching.
    target : DataFrame
        The dataframe to match against.
    on_time : str
        Column name for datetime.
    on_depth : str
        Column name for depth.
    col_name : str
        Column name of target value to bring back.
    time_tolerance : str or pd.Timedelta, optional
        Maximum allowed datetime difference (e.g. "5min").
    depth_tolerance : float, optional
        Maximum allowed depth difference (same units as depth).
    """
    # Cross join
    merged = x_df.merge(y_df, how='cross', suffixes=('_x', '_y'))   # Creates a dataframe that includes all combinations of rows from source and target
    # Differences
    merged["depth_diff"] = (merged[f"depth_x"] - merged[f"depth_y"]).abs()
    merged["time_diff"] = (merged[f"datetime_x"] - merged[f"datetime_y"]).abs().dt.total_seconds()

    # Apply tolerances
    if depth_tolerance is not None:
        merged = merged[merged["depth_diff"] <= depth_tolerance]
    if time_tolerance is not None:
        tol = pd.Timedelta(time_tolerance).total_seconds()
        merged = merged[merged["time_diff"] <= tol]

    # if merged.empty:
    #     return (
    #         pd.DataFrame(columns=["datetime", "depth", from_col_name]),
    #         pd.DataFrame(columns=from_df.columns),
    #         pd.DataFrame(columns=[from_col_name, to_col_name])
    #     )

    # Sort by depth first, then time
    merged = merged.sort_values(["depth_diff", "time_diff"])
    # Pick best match per source row
    nearest = (merged.groupby([f"datetime_x", f"depth_x"]).first().reset_index())

    x_out = nearest[[f"datetime_x", f"depth_x", x_col_name, "id_x", "type_x"]].rename(
        columns={f"datetime_x": "datetime", f"depth_x": "depth", "id_x": "id", "type_x": "type"}
    )

    y_out = nearest[[f"datetime_y", f"depth_y", y_col_name, "id_y", "type_y"]].rename(
        columns={f"datetime_y": "datetime", f"depth_y": "depth", "id_y": "id", "type_y": "type"}
    )

    return x_out, y_out

def calculate_params(x_df: pd.DataFrame,
                     x_col_name: str,
                     x_id_name: str,
                     y_df: pd.DataFrame,
                     y_col_name: str,
                     y_id_name: str,
                     time_tolerance: str,
                     depth_tolerance: float,
                     fit_intercept: bool,
                     relation: str,
                     weighted: bool):
    
    x_df_matched, y_df_matched = match_datasets(x_df=x_df,
                                                    y_df=y_df,
                                                    x_col_name=x_col_name,
                                                    y_col_name=y_col_name,
                                                    time_tolerance=time_tolerance,
                                                    depth_tolerance=depth_tolerance)
        
    y_vals = y_df_matched[y_col_name].to_numpy()
    if len(y_vals) == 0:
        return {"Error": "No valid data points found for SSC calibration"}
    if relation == "linear":
        x_vals = x_df_matched[x_col_name].to_numpy()
    else:
        x_vals = np.log10(x_df_matched[x_col_name].to_numpy())
    X = x_vals.reshape(-1, 1)
    Y = y_vals.reshape(-1, 1)
    if weighted:
        dt = (x_df_matched["datetime"] - y_df_matched["datetime"]).dt.total_seconds().abs()
        reg = LinearRegression(fit_intercept=fit_intercept).fit(X, Y, sample_weight=1/(dt+1))  # add 1 to avoid division by zero
    else:
        reg = LinearRegression(fit_intercept=fit_intercept).fit(X, Y)
    B = reg.coef_[0]
    if isinstance(B, list) or isinstance(B, np.ndarray):
        B = B[0]
    A = reg.intercept_
    if isinstance(A, list) or isinstance(A, np.ndarray):
        A = A[0]
    ssc_params = {}
    ssc_params['A'] = A
    ssc_params['B'] = B
    ssc_params['RMSE'] = np.sqrt(np.mean((A + x_vals * B - y_vals) ** 2))
    ssc_params['R2'] = reg.score(X, Y)
    ssc_params[to_id_name] = x_vals
    ssc_params[from_id_name] = y_vals
    pairs_df = pd.DataFrame({"id_from": from_df_matched["id"], "type_from": from_df_matched["type"], "id_to": to_df_matched["id"], "type_to": to_df_matched["type"]})
    pairs = (pairs_df.drop_duplicates().to_dict(orient="records"))
    # Format nicely: {"WaterSample": 26, "VesselMountedADCP": 13}
    typed_pairs = []
    for p in pairs:
        typed_pairs.append({
            p["type_from"]: p["id_from"],
            p["type_to"]: p["id_to"]
        })
    ssc_params["Pairs"] = str(typed_pairs)
    return ssc_params

if __name__ == "__main__":
    pass