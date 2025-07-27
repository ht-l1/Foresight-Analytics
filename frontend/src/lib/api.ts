import axios from "axios";

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1",
});

export const getCompanyProfile = async (symbol: string) => {
  const response = await apiClient.get(`/company/${symbol}`);
  return response.data;
};

export const getIncomeStatements = async (symbol: string, limit: number = 1) => {
  const response = await apiClient.get(
    `/financials/${symbol}/income-statements`,
    {
      params: { limit },
    }
  );
  return response.data;
};