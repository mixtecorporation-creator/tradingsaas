"use client";

import { useEffect, useRef } from "react";
import { createChart, type IChartApi, type ISeriesApi, type CandlestickSeriesPartialOptions, ColorType } from "lightweight-charts";
import type { OHLCV } from "@/lib/types";

interface PriceChartProps {
  data: OHLCV[];
  symbol?: string;
  height?: number;
}

export function PriceChart({ data, symbol, height = 400 }: PriceChartProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<"Candlestick"> | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const chart = createChart(containerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: "transparent" },
        textColor: "#6b7280",
      },
      grid: {
        vertLines: { color: "#1f2937" },
        horzLines: { color: "#1f2937" },
      },
      width: containerRef.current.clientWidth,
      height,
      crosshair: {
        mode: 0,
      },
      timeScale: {
        borderColor: "#374151",
        timeVisible: true,
        secondsVisible: false,
      },
      rightPriceScale: {
        borderColor: "#374151",
      },
    });

    const series = chart.addCandlestickSeries({
      upColor: "#22c55e",
      downColor: "#ef4444",
      borderDownColor: "#ef4444",
      borderUpColor: "#22c55e",
      wickDownColor: "#ef4444",
      wickUpColor: "#22c55e",
    } satisfies CandlestickSeriesPartialOptions);

    chartRef.current = chart;
    seriesRef.current = series;

    const handleResize = () => {
      if (containerRef.current) {
        chart.applyOptions({ width: containerRef.current.clientWidth });
      }
    };
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      chart.remove();
    };
  }, [height]);

  useEffect(() => {
    if (!seriesRef.current || !data.length) return;

    const chartData = data.map((d) => ({
      time: (new Date(d.open_time).getTime() / 1000) as any,
      open: d.open,
      high: d.high,
      low: d.low,
      close: d.close,
    })).reverse();

    seriesRef.current.setData(chartData);
  }, [data]);

  return (
    <div className="relative">
      {symbol && (
        <div className="absolute left-4 top-3 z-10">
          <span className="text-sm font-medium text-muted-foreground">{symbol}</span>
        </div>
      )}
      <div ref={containerRef} className="w-full" />
    </div>
  );
}
