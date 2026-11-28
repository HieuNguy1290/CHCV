import 'package:material_ui/material_ui.dart';
import 'package:puzzle/data/game_guides.dart';
import 'package:puzzle/data/game_guides_vi.dart';
import 'package:puzzle/l10n/app_localizations.dart';
import 'package:puzzle/utils/design_system.dart';
import 'package:puzzle/utils/l10n_game_helpers.dart';
import 'package:puzzle/widgets/tangible.dart';

class GameGuideScreen extends StatelessWidget {
  final String gameId;
  final Color gameColor;

  const GameGuideScreen({
    super.key,
    required this.gameId,
    required this.gameColor,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final l10n = AppLocalizations.of(context)!;
    final guide = gameGuides[gameId];

    if (guide == null) {
      return Scaffold(
        appBar: AppBar(title: Text(l10n.guideTitle)),
        body: Center(child: Text(l10n.guideMissing)),
      );
    }

    final isVietnamese = l10n.localeName == 'vi';
    final translation = isVietnamese ? vietnameseGameGuides[gameId] : null;
    final title = isVietnamese
        ? L10nGameHelpers.getGameTitle(context, gameId)
        : guide.title;
    final category = switch (guide.category) {
      'LOGIC' => l10n.categoryLogic,
      'MATH' => l10n.categoryMath,
      'WORD' => l10n.categoryWord,
      'MEMORY' => l10n.categoryMemory,
      'SPATIAL' => l10n.categorySpatial,
      'ATTENTION' => l10n.categoryAttention,
      'Math & Logic' => l10n.guideCategoryMathLogic,
      'Focus & Attention' => l10n.categoryAttention,
      'Language' => l10n.categoryWord,
      'Visual Spatial' => l10n.categorySpatial,
      'FLEXIBILITY' => l10n.guideCategoryFlexibility,
      'SPEED' => l10n.guideCategorySpeed,
      _ => guide.category,
    };

    return Scaffold(
      backgroundColor: theme.colorScheme.surface,
      body: SafeArea(
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 700),
            child: Column(
              children: [
                AppBar(
                  title: Text(
                    isVietnamese ? '${l10n.guideTitle} $title' : '$title ${l10n.guideTitle}',
                    style: const TextStyle(fontWeight: FontWeight.w600),
                  ),
                  backgroundColor: Colors.transparent,
                  elevation: 0,
                  leading: IconButton(
                    icon: const Icon(Icons.arrow_back_rounded),
                    onPressed: () => Navigator.of(context).pop(),
                  ),
                ),
                Expanded(
                  child: SingleChildScrollView(
                    padding: const EdgeInsets.all(DesignSystem.spaceLG),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Category Badge
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                          decoration: BoxDecoration(
                            color: gameColor.withValues(alpha: 0.15),
                            borderRadius: BorderRadius.circular(6.0),
                            border: Border.all(
                              color: gameColor.withValues(alpha: 0.3),
                              width: 1.0,
                            ),
                          ),
                          child: Text(
                            (isVietnamese ? category : guide.category).toUpperCase(),
                            style: TextStyle(
                              fontSize: 10.0,
                              fontWeight: FontWeight.w900,
                              color: gameColor,
                              letterSpacing: 1.0,
                            ),
                          ),
                        ),
                        const SizedBox(height: DesignSystem.spaceLG),

                        // Title
                        Text(
                          title,
                          style: theme.textTheme.headlineLarge?.copyWith(
                            fontWeight: FontWeight.w700,
                            letterSpacing: -0.5,
                          ),
                        ),
                        const SizedBox(height: DesignSystem.spaceSM),
                        Text(
                          l10n.guideSummary.toUpperCase(),
                          style: theme.textTheme.labelSmall?.copyWith(
                            color: theme.colorScheme.onSurface.withValues(alpha: 0.5),
                            letterSpacing: 1.2,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: DesignSystem.spaceXL),

                        // Section: Objective
                        _buildSectionHeader(context, l10n.guideObjective),
                        _buildTextCard(context, translation?.objective ?? guide.objective),
                        const SizedBox(height: DesignSystem.spaceXL),

                        // Section: Controls
                        _buildSectionHeader(context, l10n.guideControls),
                        _buildBulletList(context, [translation?.controls ?? guide.controls]),
                        const SizedBox(height: DesignSystem.spaceXL),

                        // Section: Step-by-Step Walkthrough
                        _buildSectionHeader(context, l10n.guideWalkthrough),
                        _buildNumberedList(context, translation?.walkthrough ?? guide.walkthrough),
                        const SizedBox(height: DesignSystem.spaceXL),

                        // Section: Strategies & Tips
                        _buildSectionHeader(context, l10n.guideStrategies),
                        _buildBulletList(context, translation?.strategies ?? guide.strategies),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildSectionHeader(BuildContext context, String title) {
    final theme = Theme.of(context);
    return Padding(
      padding: const EdgeInsets.only(bottom: DesignSystem.spaceMD),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: theme.textTheme.titleMedium?.copyWith(
              fontWeight: FontWeight.w700,
              letterSpacing: -0.2,
            ),
          ),
          const SizedBox(height: 4),
          Container(
            width: 40,
            height: 3,
            decoration: BoxDecoration(
              color: gameColor,
              borderRadius: BorderRadius.circular(1.5),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTextCard(BuildContext context, String text) {
    final theme = Theme.of(context);
    return TangibleContainer(
      padding: const EdgeInsets.all(DesignSystem.spaceMD),
      child: Text(
        text,
        style: theme.textTheme.bodyMedium?.copyWith(
          height: 1.5,
        ),
      ),
    );
  }

  Widget _buildBulletList(BuildContext context, List<String> items) {
    final theme = Theme.of(context);
    return Column(
      children: items.map((item) {
        return Padding(
          padding: const EdgeInsets.only(bottom: DesignSystem.spaceSM),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Padding(
                padding: const EdgeInsets.only(top: 6.0, right: 10.0),
                child: Container(
                  width: 6,
                  height: 6,
                  decoration: BoxDecoration(
                    color: gameColor,
                    shape: BoxShape.circle,
                  ),
                ),
              ),
              Expanded(
                child: Text(
                  item,
                  style: theme.textTheme.bodyMedium?.copyWith(
                    height: 1.5,
                  ),
                ),
              ),
            ],
          ),
        );
      }).toList(),
    );
  }

  Widget _buildNumberedList(BuildContext context, List<String> items) {
    final theme = Theme.of(context);
    return Column(
      children: items.asMap().entries.map((entry) {
        final idx = entry.key + 1;
        final item = entry.value;
        return Padding(
          padding: const EdgeInsets.only(bottom: DesignSystem.spaceSM),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                width: 20,
                alignment: Alignment.centerLeft,
                child: Text(
                  '$idx.',
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    color: gameColor,
                  ),
                ),
              ),
              Expanded(
                child: Text(
                  item,
                  style: theme.textTheme.bodyMedium?.copyWith(
                    height: 1.5,
                  ),
                ),
              ),
            ],
          ),
        );
      }).toList(),
    );
  }
}
