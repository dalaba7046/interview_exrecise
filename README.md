# interview_exrecise
#Q:
汽車品牌數據是樹狀結構。以BMW為例，

BMW 
- 1'
 - E81 
  - 3 Doors
   - 116d
    - ECE 
     - 11 Engine 
      - 11_4021 Short Engine 
       - Part 1
        - Part 2 

      - 11_4023 Engine block
      - 11_4099 Engine block mounting parts 
 - E82
 - E87

由於車型眾多，為了加速數據獲取，一般都會以分散式框架，平行獲取。
在第一題 我們知道n+1層數據的API 都可以在 第n層 的API裡獲得。

假設獲得的API URL 會在 30分鐘後過期，且有五隻爬蟲實例，每個爬蟲每次可以發送一個 URL 請求，
請問該如何規劃請求來達到最少重複請求(最少請求次數)

#A:
1. 每隻爬蟲實例選擇一個品牌開始：
   - 爬蟲 1: BMW
   - 爬蟲 2: 空閒
   - 爬蟲 3: 空閒
   - 爬蟲 4: 空閒
   - 爬蟲 5: 空閒

2. 每隻爬蟲依序發送請求獲得下一層的數據：
   - 爬蟲 1: 發送請求獲得 E81, E82, E87 車系
   - 爬蟲 2: 發送請求獲得 3 Doors 車型
   - 爬蟲 3: 空閒
   - 爬蟲 4: 空閒
   - 爬蟲 5: 空閒

3. 爬蟲 2 獲得車型後，發送請求獲得下一層的數據：
   - 爬蟲 1: 空閒
   - 爬蟲 2: 發送請求獲得 116d 引擎
   - 爬蟲 3: 空閒
   - 爬蟲 4: 空閒
   - 爬蟲 5: 空閒

4. 爬蟲 2 獲得引擎後，發送請求獲得下一層的數據：
   - 爬蟲 1: 空閒
   - 爬蟲 2: 發送請求獲得 ECE 地區
   - 爬蟲 3: 空閒
   - 爬蟲 4: 空閒
   - 爬蟲 5: 空閒

5. 爬蟲 2 獲得地區後，發送請求獲得下一層的數據：
   - 爬蟲 1: 空閒
   - 爬蟲 2: 發送請求獲得 11 Engine 零件分類
   - 爬蟲 3: 空閒
   - 爬蟲 4: 空閒
   - 爬蟲 5: 空閒

6. 爬蟲們逐層發送請求，獲得完整的數據結構。
