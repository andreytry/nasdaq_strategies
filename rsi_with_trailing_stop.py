//@version=5
// for 1-minute chart
//24% with 3 contracts
strategy("NASDAQ MACD + RSI Strategy with Trailing Stop", overlay=true)

// Input settings
macdSource = input(close, "MACD Source")
macdFastLength = input.int(12, "MACD Fast Length", minval=1)
macdSlowLength = input.int(26, "MACD Slow Length", minval=1)
macdSignalSmoothing = input.int(9, "MACD Signal Smoothing", minval=1)
rsiLength = input.int(14, "RSI Length", minval=1)
rsiOverbought = input.int(70, "RSI Overbought Level", minval=50, maxval=100)
rsiOversold = input.int(30, "RSI Oversold Level", minval=0, maxval=50)
lookbackPeriod = input.int(15, "RSI Lookback Period", minval=1)
trailPoints = input.float(100, "Trailing Stop Offset (Points)", minval=1)

// Calculate MACD and Signal Line
[macdLine, signalLine, _] = ta.macd(macdSource, macdFastLength, macdSlowLength, macdSignalSmoothing)

// Calculate RSI
rsi = ta.rsi(close, rsiLength)

// Define conditions
macdCrossOver = ta.crossover(macdLine, signalLine)
macdCrossUnder = ta.crossunder(macdLine, signalLine)
wasRSIOverbought = ta.highest(rsi, lookbackPeriod) > rsiOverbought
wasRSIOversold = ta.lowest(rsi, lookbackPeriod) < rsiOversold

// Entry conditions
longCondition = macdCrossOver 
shortCondition = macdCrossUnder 

// Trailing Stop Calculation for Long
if (longCondition)
    strategy.entry("Long", strategy.long)
    strategy.exit("Exit Long", "Long", trail_points=trailPoints, trail_offset=trailPoints)

// Trailing Stop Calculation for Short
if (shortCondition)
    strategy.entry("Short", strategy.short)
    strategy.exit("Exit Short", "Short", trail_points=trailPoints, trail_offset=trailPoints)

// Plot MACD and Signal
plot(macdLine, color=color.blue, title="MACD Line")
plot(signalLine, color=color.orange, title="Signal Line")
hline(0, "Zero Line", color=color.gray)
