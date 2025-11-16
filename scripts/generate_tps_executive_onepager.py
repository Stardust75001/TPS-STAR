#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import argparse
import os

def build_onepager(input_csv, output_pdf):
    metrics = pd.read_csv(input_csv)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 20, "TPS Executive Weekly OnePager", ln=1, align="C")

    pdf.set_font("Arial", "", 14)

    for col in metrics.columns:
        pdf.cell(0, 10, f"{col}: {metrics[col][0]}", ln=1)

    pdf.output(output_pdf)
    print(f"✅ Executive OnePager generated → {output_pdf}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv")
    parser.add_argument("output_pdf")
    args = parser.parse_args()

    build_onepager(args.input_csv, args.output_pdf)

if __name__ == "__main__":
    main()
