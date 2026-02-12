def operational_response(action, files_touched, commit_hash=None, risk_level='Low', next_recommendation='Monitor performance.'):
    response = {
        '🔍 Action Taken': action,
        '📦 Files Touched': files_touched,
        '📦 Git Commit Hash': commit_hash if commit_hash else 'N/A',
        '⚠️ Risk Level': risk_level,
        '🛠 Next Recommendation': next_recommendation
    }
    return response
