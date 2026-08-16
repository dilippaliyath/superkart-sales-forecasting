
import os
import requests
import pandas as pd
import streamlit as st


# =========================================================
# Application Configuration
# =========================================================

st.set_page_config(
    page_title="SuperKart Sales Forecasting",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# Backend Configuration
# =========================================================

# The backend URL is read from an environment variable.
# When running inside Docker, "backend" should be the
# backend service/container name on the shared Docker network.
BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://backend:7860"
)


# =========================================================
# Custom Styling
# =========================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .hero-card {
        padding: 1.8rem 2rem;
        border-radius: 18px;
        background: linear-gradient(
            135deg,
            rgba(20, 90, 160, 0.12),
            rgba(0, 180, 150, 0.08)
        );
        border: 1px solid rgba(120, 120, 120, 0.18);
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-size: 2.3rem;
        font-weight: 750;
        margin-bottom: 0.35rem;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        opacity: 0.78;
        margin-bottom: 0;
    }

    .section-card {
        padding: 1.25rem;
        border-radius: 14px;
        border: 1px solid rgba(120, 120, 120, 0.18);
        margin-bottom: 1rem;
    }

    .prediction-card {
        padding: 1.6rem;
        border-radius: 16px;
        text-align: center;
        border: 1px solid rgba(120, 120, 120, 0.18);
        background: rgba(0, 180, 150, 0.08);
        margin-top: 1rem;
    }

    .prediction-label {
        font-size: 1rem;
        opacity: 0.75;
    }

    .prediction-value {
        font-size: 2.2rem;
        font-weight: 750;
        margin-top: 0.25rem;
    }

    div[data-testid="stButton"] > button {
        width: 100%;
        border-radius: 10px;
        min-height: 3rem;
        font-weight: 650;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# Header
# =========================================================

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">🛒 SuperKart Sales Forecasting</div>
        <div class="hero-subtitle">
            Predict product-store sales revenue using product,
            pricing, and store characteristics.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# Sidebar
# =========================================================

with st.sidebar:

    st.header("SuperKart")

    st.write(
        "Use the application to generate sales forecasts "
        "for individual products or upload a CSV file for "
        "batch forecasting."
    )

    st.divider()

    st.caption("Prediction Service")

    # Optional backend health check
    if st.button("Check API Status"):

        try:
            response = requests.get(
                f"{BACKEND_URL}/",
                timeout=10
            )

            if response.status_code == 200:
                st.success("Backend API is online")
            else:
                st.warning(
                    f"Backend responded with status "
                    f"{response.status_code}"
                )

        except requests.exceptions.RequestException:
            st.error("Backend API is unavailable")


# =========================================================
# Main Tabs
# =========================================================

single_tab, batch_tab = st.tabs(
    [
        "📈 Single Prediction",
        "📂 Batch Prediction"
    ]
)


# =========================================================
# SINGLE PREDICTION
# =========================================================

with single_tab:

    st.subheader("Product and Store Information")

    st.caption(
        "Enter the product and store characteristics below."
    )

    # -----------------------------------------------------
    # Product Information
    # -----------------------------------------------------

    st.markdown("### Product Details")

    col1, col2, col3 = st.columns(3)

    with col1:

        Product_Weight = st.number_input(
            "Product Weight",
            min_value=0.0,
            value=12.66,
            step=0.1,
            help="Weight of the product."
        )

        Product_Sugar_Content = st.selectbox(
            "Sugar Content",
            [
                "Low Sugar",
                "Regular",
                "No Sugar"
            ]
        )

    with col2:

        Product_Allocated_Area = st.number_input(
            "Allocated Display Area",
            min_value=0.0,
            max_value=1.0,
            value=0.068,
            step=0.001,
            format="%.3f",
            help=(
                "Ratio of product display area to the "
                "total display area in the store."
            )
        )

        Product_MRP = st.number_input(
            "Product MRP",
            min_value=0.0,
            value=147.00,
            step=1.0
        )

    with col3:

        Product_Type = st.selectbox(
            "Product Type",
            [
                "Fruits and Vegetables",
                "Snack Foods",
                "Frozen Foods",
                "Dairy",
                "Household",
                "Baking Goods",
                "Canned",
                "Health and Hygiene",
                "Meat",
                "Soft Drinks",
                "Breads",
                "Hard Drinks",
                "Others",
                "Starchy Foods",
                "Breakfast",
                "Seafood"
            ]
        )

        Product_Id_Prefix = st.selectbox(
            "Product ID Prefix",
            [
                "FD",
                "DR",
                "NC"
            ],
            help="Two-character prefix extracted from Product_Id."
        )


    st.divider()


    # -----------------------------------------------------
    # Store Information
    # -----------------------------------------------------

    st.markdown("### Store Details")

    col4, col5, col6 = st.columns(3)

    with col4:

        Store_Id = st.selectbox(
            "Store ID",
            [
                "OUT001",
                "OUT002",
                "OUT003",
                "OUT004"
            ]
        )

        Store_Size = st.selectbox(
            "Store Size",
            [
                "Small",
                "Medium",
                "High"
            ]
        )

    with col5:

        Store_Location_City_Type = st.selectbox(
            "City Tier",
            [
                "Tier 1",
                "Tier 2",
                "Tier 3"
            ]
        )

        Store_Type = st.selectbox(
            "Store Type",
            [
                "Departmental Store",
                "Supermarket Type1",
                "Supermarket Type2",
                "Food Mart"
            ]
        )

    with col6:

        Store_Age = st.number_input(
            "Store Age",
            min_value=0,
            value=16,
            step=1,
            help="Age of the store in years."
        )


    # -----------------------------------------------------
    # JSON Payload
    # -----------------------------------------------------

    product_data = {

        "Product_Weight": Product_Weight,

        "Product_Sugar_Content":
            Product_Sugar_Content,

        "Product_Allocated_Area":
            Product_Allocated_Area,

        "Product_Type":
            Product_Type,

        "Product_MRP":
            Product_MRP,

        "Store_Id":
            Store_Id,

        "Store_Size":
            Store_Size,

        "Store_Location_City_Type":
            Store_Location_City_Type,

        "Store_Type":
            Store_Type,

        "Product_Id_Prefix":
            Product_Id_Prefix,

        "Store_Age":
            Store_Age
    }


    st.write("")

    predict_col1, predict_col2, predict_col3 = st.columns(
        [1, 2, 1]
    )

    with predict_col2:

        predict_button = st.button(
            "Generate Sales Forecast",
            type="primary"
        )


    # -----------------------------------------------------
    # Prediction Request
    # -----------------------------------------------------

    if predict_button:

        try:

            with st.spinner(
                "Generating sales forecast..."
            ):

                response = requests.post(
                    f"{BACKEND_URL}/v1/predict",
                    json=product_data,
                    timeout=30
                )


            if response.status_code == 200:

                result = response.json()

                predicted_sales = float(
                    result["Sales"]
                )

                st.markdown(
                    f"""
                    <div class="prediction-card">
                        <div class="prediction-label">
                            Predicted Product-Store Sales
                        </div>
                        <div class="prediction-value">
                            ₹{predicted_sales:,.2f}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.success(
                    "Sales forecast generated successfully."
                )

            else:

                try:
                    error_message = response.json()
                except Exception:
                    error_message = response.text

                st.error(
                    f"Prediction failed: {error_message}"
                )


        except requests.exceptions.Timeout:

            st.error(
                "The prediction service took too long "
                "to respond. Please try again."
            )


        except requests.exceptions.ConnectionError:

            st.error(
                "Unable to connect to the SuperKart "
                "prediction service."
            )


        except requests.exceptions.RequestException as e:

            st.error(
                f"Prediction service error: {e}"
            )


# =========================================================
# BATCH PREDICTION
# =========================================================

with batch_tab:

    st.subheader("Batch Sales Forecasting")

    st.write(
        "Upload a CSV file containing multiple product-store "
        "records to generate sales predictions in one request."
    )

    st.info(
        """
        The CSV file should contain the following columns:

        Product_Weight, Product_Sugar_Content,
        Product_Allocated_Area, Product_Type,
        Product_MRP, Store_Id, Store_Size,
        Store_Location_City_Type, Store_Type,
        Product_Id_Prefix, Store_Age
        """
    )


    uploaded_file = st.file_uploader(
        "Upload prediction CSV",
        type=["csv"],
        help="Upload a CSV file containing the required features."
    )


    if uploaded_file is not None:

        # Preview uploaded data
        try:

            preview_df = pd.read_csv(uploaded_file)

            st.markdown("### Data Preview")

            st.dataframe(
                preview_df.head(10),
                use_container_width=True
            )

            st.caption(
                f"{preview_df.shape[0]:,} rows × "
                f"{preview_df.shape[1]} columns"
            )

            # Reset file pointer before API request
            uploaded_file.seek(0)

        except Exception as e:

            st.error(
                f"Unable to preview CSV file: {e}"
            )


        if st.button(
            "Generate Batch Forecast",
            type="primary"
        ):

            try:

                uploaded_file.seek(0)

                with st.spinner(
                    "Generating batch predictions..."
                ):

                    response = requests.post(
                        f"{BACKEND_URL}/v1/predictbatch",
                        files={
                            "file": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                "text/csv"
                            )
                        },
                        timeout=120
                    )


                if response.status_code == 200:

                    results = response.json()

                    # Backend returns:
                    # {"0": prediction, "1": prediction, ...}

                    if isinstance(results, dict):

                        predictions_df = pd.DataFrame(
                            {
                                "Row": [
                                    int(index)
                                    for index
                                    in results.keys()
                                ],
                                "Predicted_Sales": [
                                    float(value)
                                    for value
                                    in results.values()
                                ]
                            }
                        )

                        predictions_df = (
                            predictions_df
                            .sort_values("Row")
                            .reset_index(drop=True)
                        )

                    elif isinstance(results, list):

                        predictions_df = pd.DataFrame(
                            {
                                "Predicted_Sales":
                                    results
                            }
                        )

                    else:

                        predictions_df = pd.DataFrame(
                            {
                                "Predicted_Sales":
                                    [results]
                            }
                        )


                    st.success(
                        f"Successfully generated "
                        f"{len(predictions_df):,} predictions."
                    )


                    st.markdown(
                        "### Prediction Results"
                    )

                    st.dataframe(
                        predictions_df,
                        use_container_width=True
                    )


                    # Download predictions
                    csv_output = (
                        predictions_df
                        .to_csv(index=False)
                        .encode("utf-8")
                    )

                    st.download_button(
                        label="Download Predictions",
                        data=csv_output,
                        file_name=(
                            "superkart_sales_predictions.csv"
                        ),
                        mime="text/csv",
                        use_container_width=True
                    )


                else:

                    try:
                        error_message = response.json()
                    except Exception:
                        error_message = response.text

                    st.error(
                        f"Batch prediction failed: "
                        f"{error_message}"
                    )


            except requests.exceptions.Timeout:

                st.error(
                    "The batch prediction request timed out. "
                    "Try a smaller file or try again."
                )


            except requests.exceptions.ConnectionError:

                st.error(
                    "Unable to connect to the "
                    "SuperKart prediction service."
                )


            except requests.exceptions.RequestException as e:

                st.error(
                    f"Prediction service error: {e}"
                )


# =========================================================
# Footer
# =========================================================

st.divider()

st.caption(
    "SuperKart Sales Forecasting System • "
    "Machine Learning Powered Revenue Prediction"
)
