import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { settingsApi } from '../services/settingsApi';
import { AppSettings } from '../types/project';

export const SETTINGS_QUERY_KEY = ['settings'];

export const useSettings = () => {
  const queryClient = useQueryClient();

  const settingsQuery = useQuery({
    queryKey: SETTINGS_QUERY_KEY,
    queryFn: settingsApi.getSettings,
  });

  const updateMutation = useMutation({
    mutationFn: (data: Partial<AppSettings>) => settingsApi.updateSettings(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: SETTINGS_QUERY_KEY });
    },
  });

  return {
    settings: settingsQuery.data,
    isLoading: settingsQuery.isLoading,
    isError: settingsQuery.isError,
    updateSettings: updateMutation.mutateAsync,
    isUpdating: updateMutation.isPending,
  };
};
