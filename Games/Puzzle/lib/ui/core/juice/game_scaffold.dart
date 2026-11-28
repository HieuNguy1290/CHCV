import 'package:material_ui/material_ui.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:wakelock_plus/wakelock_plus.dart';
import 'dart:math' as math;
import 'package:puzzle/l10n/app_localizations.dart';
import '../../../utils/design_system.dart';
import '../../../widgets/tangible.dart';
import '../../../data/game_registry.dart';
import '../../../providers/user_providers.dart';

class GameScaffold extends ConsumerStatefulWidget {
  final String title;
  final Widget body;
  final List<Widget>? actions;
  final Widget? bottomNavigationBar;
  final Widget? floatingActionButton;
  final String? subtitle;
  final VoidCallback? onHowToPlay;
  final VoidCallback? onReset;

  const GameScaffold({
    super.key,
    required this.title,
    required this.body,
    this.actions,
    this.bottomNavigationBar,
    this.floatingActionButton,
    this.subtitle,
    this.onHowToPlay,
    this.onReset,
  });

  @override
  ConsumerState<GameScaffold> createState() => _GameScaffoldState();
}

class _GameScaffoldState extends ConsumerState<GameScaffold> {
  bool _wakelockActive = false;

  @override
  void dispose() {
    if (_wakelockActive) {
      WakelockPlus.disable();
    }
    super.dispose();
  }

  void _syncWakelock(bool keepAwake) {
    if (keepAwake != _wakelockActive) {
      _wakelockActive = keepAwake;
      if (keepAwake) {
        WakelockPlus.enable();
      } else {
        WakelockPlus.disable();
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final keepAwake = ref.watch(
      userDataNotifierProvider.select((u) => u.isKeepScreenAwakeEnabled ?? false),
    );
    _syncWakelock(keepAwake);

    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final mediaQuery = MediaQuery.of(context);
    final isMobile = DesignSystem.isMobile(context);
    
    // Calculate a responsive max width.
    // For games, we don't want the board to be wider than the available height
    // to prevent vertical overflow with AspectRatio(1) widgets.
    final availableHeight = mediaQuery.size.height - mediaQuery.padding.top - mediaQuery.padding.bottom - kToolbarHeight;
    final responsiveMaxWidth = math.min(600.0, availableHeight * 0.85);

    return Scaffold(
      backgroundColor: colorScheme.surface,
      body: SafeArea(
        child: Center(
          child: ConstrainedBox(
            constraints: BoxConstraints(maxWidth: isMobile ? double.infinity : math.max(400.0, responsiveMaxWidth)),
            child: Column(
              children: [
                _buildAppBar(context),
                Expanded(child: widget.body),
              ],
            ),
          ),
        ),
      ),
      bottomNavigationBar: widget.bottomNavigationBar != null
          ? SafeArea(
              child: Center(
                child: ConstrainedBox(
                  constraints: BoxConstraints(maxWidth: isMobile ? double.infinity : math.max(400.0, responsiveMaxWidth)),
                  child: widget.bottomNavigationBar,
                ),
              ),
            )
          : null,
      floatingActionButton: widget.floatingActionButton,
    );
  }

  Widget _buildAppBar(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Container(
      padding: const EdgeInsets.fromLTRB(
        DesignSystem.spaceMD,
        DesignSystem.spaceSM,
        DesignSystem.spaceMD,
        DesignSystem.spaceXS,
      ),
      child: Row(
        children: [
          // Back button: simple, modern, borderless flat scaling button
          TangibleButton(
            color: Colors.transparent,
            drawBorder: false,
            onTap: () => Navigator.of(context).pop(),
            padding: const EdgeInsets.all(12),
            child: Icon(
              Icons.arrow_back_ios_new_rounded,
              color: colorScheme.onSurface,
              size: 22,
            ),
          ),
          const SizedBox(width: DesignSystem.spaceSM),
          Expanded(
            child: Center(
              child: FittedBox(
                fit: BoxFit.scaleDown,
                alignment: Alignment.center,
                child: Text(
                  widget.title.toUpperCase(),
                  style: TextStyle(
                    fontFamily: DesignSystem.fontDisplay,
                    fontSize: DesignSystem.fontSize2XL,
                    letterSpacing: 1.2,
                    fontWeight: FontWeight.w700,
                    color: colorScheme.onSurface,
                  ),
                ),
              ),
            ),
          ),
          // Info / Help button: always shown for every game!
          const SizedBox(width: DesignSystem.spaceSM),
          TangibleButton(
            color: Colors.transparent,
            drawBorder: false,
            onTap: widget.onHowToPlay ?? () => _showDefaultHelpDialog(context),
            padding: const EdgeInsets.all(12),
            child: Icon(
              Icons.info_outline_rounded,
              color: colorScheme.onSurface,
              size: 22,
            ),
          ),
        ],
      ),
    );
  }

  void _showDefaultHelpDialog(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    final l10n = AppLocalizations.of(context)!;

    // Resolve detailed descriptive subtitle
    String? resolvedSubtitle = widget.subtitle;
    String? gameId;
    try {
      final matchingGame = allGamesMetadata.firstWhere(
        (g) => g.titleGetter(context).toUpperCase() == widget.title.toUpperCase(),
      );
      gameId = matchingGame.id;
      if (resolvedSubtitle == null || resolvedSubtitle.toUpperCase() == widget.title.toUpperCase()) {
        resolvedSubtitle = matchingGame.subtitleGetter(context);
      }
    } catch (_) {
      // Fallback
    }

    final rules = switch (gameId) {
      'kakuro' => l10n.helpKakuroRules,
      'futoshiki' => l10n.helpFutoshikiRules,
      'akari' => l10n.helpAkariRules,
      'sudoku' => l10n.helpSudokuRules,
      'alphabet_sudoku' => l10n.helpAlphabetSudokuRules,
      'slitherlink' => l10n.helpSlitherlinkRules,
      'bridges' => l10n.helpBridgesRules,
      'kenken' => l10n.helpKenkenRules,
      'nurikabe' => l10n.helpNurikabeRules,
      'hitori' => l10n.helpHitoriRules,
      'nonogram' => l10n.helpNonogramRules,
      'skyscrapers' => l10n.helpSkyscrapersRules,
      'dominosa' => l10n.helpDominosaRules,
      'lighthouses' => l10n.helpLighthousesRules,
      'magnets' => l10n.helpMagnetsRules,
      'change_blindness' => l10n.helpChangeBlindnessRules,
      'semantic_distance' => l10n.helpSemanticDistanceRules,
      _ => null,
    };
    final rulesList = rules?.split('\n');

    showDialog(
      context: context,
      builder: (context) {
        return Dialog(
          backgroundColor: Colors.transparent,
          elevation: 0,
          insetPadding: const EdgeInsets.symmetric(horizontal: DesignSystem.spaceLG),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 380),
            child: TangibleContainer(
              radius: DesignSystem.radiusLG,
              padding: const EdgeInsets.all(DesignSystem.spaceLG),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        Icons.info_outline_rounded,
                        color: colorScheme.primary,
                        size: 32,
                      ),
                      const SizedBox(width: DesignSystem.spaceSM),
                      Text(
                        l10n.howToPlay.toUpperCase(),
                        style: TextStyle(
                          fontFamily: DesignSystem.fontDisplay,
                          fontSize: DesignSystem.fontSize2XL,
                          letterSpacing: 1.2,
                          fontWeight: FontWeight.w700,
                          color: colorScheme.primary,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: DesignSystem.spaceMD),
                  Text(
                    widget.title.toUpperCase(),
                    textAlign: TextAlign.center,
                    style: theme.textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.w900,
                      letterSpacing: 1.0,
                    ),
                  ),
                  const SizedBox(height: DesignSystem.spaceMD),
                  Flexible(
                    child: SingleChildScrollView(
                      child: Container(
                        width: double.infinity,
                        padding: const EdgeInsets.all(DesignSystem.spaceMD),
                        decoration: BoxDecoration(
                          color: colorScheme.onSurface.withValues(alpha: 0.05),
                          borderRadius: BorderRadius.circular(DesignSystem.radiusMD),
                          border: Border.all(
                            color: colorScheme.outline.withValues(alpha: 0.2),
                          ),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              resolvedSubtitle ?? l10n.helpDefaultObjective,
                              textAlign: TextAlign.center,
                              style: theme.textTheme.bodyMedium?.copyWith(
                                color: colorScheme.onSurface.withValues(alpha: 0.9),
                                fontSize: 14.0,
                                height: 1.4,
                              ),
                            ),
                            if (rulesList != null && rulesList.isNotEmpty) ...[
                              const SizedBox(height: DesignSystem.spaceMD),
                              Divider(color: colorScheme.outline.withValues(alpha: 0.3), height: 1),
                              const SizedBox(height: DesignSystem.spaceMD),
                              Text(
                                l10n.helpRulesHeading.toUpperCase(),
                                style: TextStyle(
                                  fontSize: DesignSystem.fontSizeSM,
                                  fontWeight: FontWeight.w900,
                                  color: colorScheme.primary,
                                  letterSpacing: 0.8,
                                ),
                              ),
                              const SizedBox(height: DesignSystem.spaceSM),
                              ...rulesList.map((rule) => Padding(
                                padding: const EdgeInsets.only(bottom: DesignSystem.spaceXS),
                                child: Row(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      "• ",
                                      style: TextStyle(
                                        fontWeight: FontWeight.bold,
                                        color: colorScheme.primary,
                                      ),
                                    ),
                                    Expanded(
                                      child: Text(
                                        rule,
                                        style: theme.textTheme.bodyMedium?.copyWith(
                                          color: colorScheme.onSurface.withValues(alpha: 0.8),
                                          fontSize: 13.0,
                                          height: 1.35,
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              )),
                            ],
                          ],
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: DesignSystem.spaceLG),
                  TangibleButton(
                    color: colorScheme.primary,
                    width: double.infinity,
                    onTap: () => Navigator.of(context).pop(),
                    child: Center(
                      child: Text(
                        l10n.gotIt.toUpperCase(),
                        style: TextStyle(
                          color: colorScheme.onPrimary,
                          fontWeight: FontWeight.w900,
                          letterSpacing: 1.0,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}

