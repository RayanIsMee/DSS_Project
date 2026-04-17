<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

    <xsl:output method="html" encoding="UTF-8" indent="yes"/>

    <!-- ================= MAIN TEMPLATE ================= -->
    <xsl:template match="/">

        <html>
            <head>
                <!-- ✅ CSS from Flask static folder -->
                <link rel="stylesheet" href="/static/style.css"/>
            </head>

            <body>

                <!-- HEADER -->
                <div class="header-info">
                    TP réalisé par : Benkaci Ali Doua | Chikhi Aya | Bouguerra Rayan
                    Groupe : 08
                </div>


                <!-- TITLE -->
                <div class="main-header">
                    <h1 class="big-title">
                        TRAIN <span>SERVICE</span> BOOKING
                    </h1>
                    <p class="sub-title">OFFICIAL SCHEDULE DOCUMENT</p>
                </div>
                <div style="text-align:center; margin-bottom:20px;">
                   <a href="/" class="btn">🔍 Rechercher un trajet</a>
                </div>


                <div class="container">

                    <!-- LOOP LINES -->
                    <xsl:for-each select="transport/lines/line">

                        <xsl:variable name="depCode" select="@departure"/>
                        <xsl:variable name="arrCode" select="@arrival"/>

                        <div class="card">

                            <!-- LINE HEADER -->
                            <div class="line-title">
                                <span class="line-badge">
                                    <xsl:value-of select="@code"/>
                                </span>

                                <span class="line-route">
                                    <xsl:value-of select="/transport/stations/station[@id=$depCode]/@name"/>
                                    →
                                    <xsl:value-of select="/transport/stations/station[@id=$arrCode]/@name"/>
                                </span>
                            </div>

                            <!-- LOOP TRIPS -->
                            <xsl:for-each select="trips/trip">

                                <div class="trip-info">

                                    <span class="trip-title">

                                        <span class="trip-code">
                                            <xsl:value-of select="@code"/>
                                        </span>

                                        <xsl:text> </xsl:text>

                                        <xsl:value-of select="/transport/stations/station[@id=$depCode]/@name"/>
                                        →
                                        <xsl:value-of select="/transport/stations/station[@id=$arrCode]/@name"/>

                                    </span>

                                    <!-- DAYS -->
                                    <span class="days-container">

                                        <span class="calendar-icon">📅</span>

                                        <xsl:call-template name="split-days">
                                            <xsl:with-param name="text" select="days"/>
                                        </xsl:call-template>

                                    </span>

                                </div>

                                <!-- TABLE -->
                                <table>

                                    <thead>
                                        <tr>
                                            <th>Schedule</th>
                                            <th>Train</th>
                                            <th>Class</th>
                                            <th>Price (DA)</th>
                                            <th>Action</th>
                                        </tr>
                                    </thead>

                                    <tbody>

                                        <!-- CLASS LOOP -->
                                        <xsl:for-each select="class">

                                            <tr>

                                                <!-- SCHEDULE -->
                                                <td>
                                                    <span class="time-box">
                                                        <span class="time-dep">
                                                            <xsl:value-of select="../schedule/@departure"/>
                                                        </span>

                                                        <span class="time-sep">→</span>

                                                        <span class="time-arr">
                                                            <xsl:value-of select="../schedule/@arrival"/>
                                                        </span>
                                                    </span>
                                                </td>

                                                <!-- TRAIN -->
                                                <td>
                                                    <span class="train-badge">
                                                        <xsl:value-of select="../@type"/>
                                                    </span>
                                                </td>

                                                <!-- CLASS -->
                                                <td>
                                                    <xsl:choose>
                                                        <xsl:when test="@type='VIP'">
                                                            <span class="vip-badge">★ VIP</span>
                                                        </xsl:when>
                                                        <xsl:otherwise>
                                                            <span class="class-badge">
                                                                <xsl:value-of select="@type"/>
                                                            </span>
                                                        </xsl:otherwise>
                                                    </xsl:choose>
                                                </td>

                                                <!-- PRICE -->
                                                <td class="price">

                                                    <xsl:variable name="priceClean">
                                                        <xsl:value-of select="translate(@price,'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz','')"/>
                                                    </xsl:variable>

                                                    <span class="amount">
                                                        <xsl:value-of select="$priceClean"/>
                                                    </span>

                                                    <span class="currency">DA</span>

                                                </td>

                                                <!-- BUTTON -->
                                                <td>
                                                    <button class="btn">Réserver</button>
                                                </td>

                                            </tr>

                                        </xsl:for-each>

                                    </tbody>

                                </table>

                            </xsl:for-each>

                        </div>

                    </xsl:for-each>

                </div>

            </body>
        </html>

    </xsl:template>

    <!-- ================= SPLIT DAYS ================= -->
    <xsl:template name="split-days">

        <xsl:param name="text"/>

        <xsl:choose>

            <xsl:when test="contains($text, ',')">

                <span class="day-pill">
                    <xsl:value-of select="substring-before($text, ',')"/>
                </span>

                <xsl:text> </xsl:text>

                <xsl:call-template name="split-days">
                    <xsl:with-param name="text" select="substring-after($text, ',')"/>
                </xsl:call-template>

            </xsl:when>

            <xsl:otherwise>

                <span class="day-pill">
                    <xsl:value-of select="$text"/>
                </span>

            </xsl:otherwise>

        </xsl:choose>

    </xsl:template>

</xsl:stylesheet>

