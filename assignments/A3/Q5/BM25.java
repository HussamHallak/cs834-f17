public class BM25 {
public  double b = 0.75;
  double k = 1.2;
  double collectionLength = 10000000.0;
  double documentCount = 100000.0;
  double documentFrequency = 1000.0;
  double idf;
  idf = Math.log((documentCount - documentFrequency + 0.5) / (documentFrequency + 0.5));
  
  public double getScore(int count, int length) {
    return idf * (count * (k + 1)) / (count + (k * (1 - b + (b * length / (collectionLength / documentCount)))));
  }
}